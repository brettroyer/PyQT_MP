"""Module containing the *ThreadWorker* class."""
import multiprocessing
import time

from PyQt5.QtCore import QObject, pyqtSignal
# from ray.util.queue import Queue
from multiprocessing import Queue
from multiprocessing import Manager

from app.helpers.process_instructions import QuitProcessing
from app.processes.process_supervisor import ProcessSupervisor
from app.processes.data_generator import DataGenerator


class ThreadWorker(QObject):
    """Class to handle work on another thread

    In this case, calling and communicating with *ParallelSupervisor*
    which will run in its own process."""

    result = pyqtSignal(str)
    status = pyqtSignal(dict)

    def __init__(self, result_function: callable, status_function: callable) -> None:
        """Initialzie the class.

        Args:
            callback_function: The function responsible for updating the view.
        """

        super().__init__()

        self.result.connect(result_function)
        self.status.connect(status_function)

        self.manager = Manager()
        self._data_queue = self.manager.Queue()  # Data for processes to consume
        self._instruction_queue = Queue()  # Instructions like start/stop/etc. for process(s) to consume. Note:  some multiprocess need there own instructions queue.
        self._result_queue = self.manager.Queue()  # Results from process(s)
        self._gen = None  # Data generator
        self.processes = []  # List of processes
        self._instruction_queues = []  # List of instruction queues.

        self._is_running = False

    def start(self) -> None:
        """Start the parallel processing."""

        self._start_process_supervisor()
        self._process_data()

    def _start_process_supervisor(self) -> None:
        """Run parallel supervisor.

        **NOTE:** *ParallelSupervisor* is instantiated here,
          rather than in the constructor, so that it happens
          **after** this worker has been moved to the *QThread* in
          *Model*.
        """
        # DataGenerator
        self._gen = DataGenerator(self._instruction_queue, self._data_queue)
        self._gen.start()

        for x in range(multiprocessing.cpu_count()):
            instruction_queue = Queue()  # Each have to have there own instruction Queue - To Process
            info = {
                "count": 1
            }
            p = ProcessSupervisor(instruction_queue, self._result_queue, self._data_queue, info)
            p.name = f"Process {x}"
            p.start()
            self.processes.append(p)
            self._instruction_queues.append(instruction_queue)

        self._is_running = True

    def _process_data(self) -> None:
        """Process the data."""

        while self._is_running:
            latest_result = self._result_queue.get()
            self.result.emit(latest_result)

        print("Process Data Thread Complete")

    def quit(self) -> None:
        """Quit parallel processing."""

        self._is_running = False  # Note:  As to be first :O

        for instruction in self._instruction_queues:
            instruction.put(QuitProcessing())

        print("Wait on Sub-Processes to Complete")
        for p in self.processes:
            p.join()

        self._instruction_queue.put(QuitProcessing())
        print("Wait on DataGenerator Process to Complete")
        self._gen.join()

        print("All Processes Complete!!")


