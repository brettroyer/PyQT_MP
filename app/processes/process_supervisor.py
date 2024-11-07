"""Module containing the *ParallelSupervisor* class.

- Here, we are using [Ray](https://www.ray.io/)
- This could be Python [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- Or something else...
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from multiprocessing import Queue
    from typing import NamedTuple

from multiprocessing import Process

from app.helpers.process_instructions import QuitProcessing
from app.helpers.view_instructions import ProcessStatusSignal


class ProcessSupervisor(Process):
    """Class to demonstrate some parallel processing."""
    # TODO: Add Status Queue

    def __init__(self, instruction_queue: Queue, result_queue: Queue, data_queue, info: dict = None) -> None:
        """Initialize the class."""
        Process.__init__(self)

        self._instruction_queue = instruction_queue
        self._result_queue = result_queue
        self._data_queue = data_queue
        self.info = info
        self._is_running = False
        # self._result_queue.put(ProcessStatusSignal(f"{self.name} Created!!"))  # Signal Only Takes String,   Update to Named Tuple

    def run(self) -> None:
        """Create data."""

        self._is_running = True

        while self._is_running:
            self._process_latest_instructions()
            self._process_data()

    def _process_latest_instructions(self) -> None:
        """Process any latest instructions.
        
        **NOTE:**
        - This is designed to process *all* instructions in the queue
          before continuing.
        - This will be useful if multiple instruction types are ever added
          to the functionality.
        """

        while not self._instruction_queue.empty():
            self._process_instruction(self._instruction_queue.get())

    def _process_instruction(self, instruction: NamedTuple) -> None:
        """Process an instruction.

        Args:
            instruction: The instruction to process.
        
        **Note:**
        - This allows for more instruction to easily be added.
        - The additonal instructions can contain fields with additional arguments.
        """

        INSTRUCTIONS = {
            QuitProcessing: self._quit
        }

        INSTRUCTIONS[type(instruction)](instruction)
    
    def _quit(self, *args) -> None:
        """Quit processing."""

        # Demonstrates, in the console, this is quitting in its separate process
        print(f"{self.name} is quitting...")
        self._is_running = False  # Must Process First before any other functions

    def _process_data(self) -> None:
        """Get the latest data and put it on the queue."""

        # result = self._data_generator.get_latest_data()

        # Demonstrates, in the console, it is running on a
        # separate process to the GUI.
        # print(result)
        if self._is_running:
            count = self._data_queue.get() + self.info['count']
            # self._result_queue.put(str(count))
            self._result_queue.put(f"{self.name}-{count}")

