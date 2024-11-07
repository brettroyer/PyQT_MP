"""Module containing the *ViewModel* class."""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.model.model import Model

from PyQt5.QtCore import QObject, pyqtSignal

from app.helpers.view_instructions import (
    UpdateSignal, ProcessStartedSignal, ProcessQuitSignal, ProcessStatusSignal)
from app.model.model import Model


class ViewModel(QObject):
    """A layer of separation between the *view* and *model*."""

    signal = pyqtSignal(tuple)

    def __init__(self) -> None:
        
        super().__init__()

        self._model = Model(self._update_view, self._update_status)
        self._is_processing = False

    def start_button_clicked(self, checked: bool) -> None:
        """Start button clicked slot."""

        if checked:
            self._model.start()
            self.signal.emit(ProcessStartedSignal())
            self._is_processing = True
        else:
            self._model.quit()
            self.signal.emit(ProcessQuitSignal())
            self._is_processing = False
    
    def _update_view(self, value: str) -> None:
        """The callback function to update the view."""

        self.signal.emit(UpdateSignal(value=value))

    def _update_status(self, status: dict) -> None:
        """The callback function to update the view
        with status info from process(s)."""

        self.signal.emit(ProcessStatusSignal(status=status))

