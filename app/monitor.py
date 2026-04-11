"""
@file:    monitor.py
@author:  Rob Pellegrin
@date:    03-18-2026

@updated: 04-10-2026

"""

import logging
import time
from pathlib import Path

log = logging.getLogger(__name__)


class LogMonitor:

    def __init__(self, file: Path):
        self._file: Path = file

        # Track last modification time.
        self._mtime: float = 0.0
        self._last_check: float = 0.0
        self._poll_interval = 1.0

    def read(self) -> list[str]:
        with open(self._file, 'r', encoding='UTF-8') as file:
            return list(file.readlines())

    def has_changed(self) -> bool:
        now = time.time()

        # Limit stat calls
        if self._last_check is not None:
            if now - self._last_check < self._poll_interval:
                return False

        mtime = self._file.stat().st_mtime
        self._last_check = time.time()

        if self._mtime is None or self._mtime != mtime:
            self._mtime = mtime
            return True

        return False

    def time_since_last_change(self) -> int:
        return int(time.time() - self._mtime)

    def __iter__(self):
        return iter(self.read())

    @property
    def name(self) -> str:
        return str(self._file.name)
