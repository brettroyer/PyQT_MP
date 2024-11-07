"""Modules containing view instruction NamedTuple classes."""

from typing import NamedTuple


class UpdateSignal(NamedTuple):
    """Indicates a new value is available for the view."""

    value: str


class ProcessStartedSignal(NamedTuple):
    """Indicates, to the view, the process has started."""


class ProcessQuitSignal(NamedTuple):
    """Indicates, to the view, the process has been quit."""


class ProcessStatusSignal(NamedTuple):
    """
    Indicates, to the view, the status of the process
    """
    status: dict

