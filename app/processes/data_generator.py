from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from multiprocessing import Queue
    from typing import NamedTuple

import time
from multiprocessing import Process
from app.helpers.process_instructions import QuitProcessing


class _DataGenerator:
    """Class to generate data."""

    def __init__(self) -> None:

        self._counter = 0

    def get_latest_data(self) -> int:
        """Get the latest data."""

        latest_count = self._counter
        self._counter += 1
        time.sleep(1)
        return latest_count


class DataGenerator(Process):

    def __init__(self, instruction_queue: Queue, result_queue: Queue, info: dict = None):
        Process.__init__(self)
        self._instruction_queue = instruction_queue
        self.result_queue = result_queue
        self.info = info
        self._counter = 0
        self._is_running = False

    def run(self) -> None:
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

    def _process_data(self) -> None:
        """Get the latest data."""

        latest_count = self._counter
        self._counter += 1
        time.sleep(1)
        self.result_queue.put(latest_count)

    def _quit(self, *args) -> None:
        """Quit processing."""

        # Demonstrates, in the console, this is quitting in its separate process
        print("DataGenerator is quitting...")

        self._is_running = False  # Must Process First before any other functions