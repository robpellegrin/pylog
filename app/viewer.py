"""
@file:    log_viewer.py
@author:  Rob Pellegrin
@date:    03-23-2026
@updated: 03-24-2026
"""

import curses
import logging
import re
from collections import namedtuple
from typing import Optional

from utils.log_monitor import LogMonitor

log = logging.getLogger(__name__)

LogLine = namedtuple("LogLine", ["date", "level", "message"])


class LogViewer:
    LOG_COLOR_MAP = {
        "[INFO]": 1,
        "[DEBUG]": 2,
        "[WARNING]": 3,
        "[ERROR]": 4,
        "[CRITICAL]": 5,
    }

    VIEW_TOP = 3

    def __init__(self, app):
        self.stdscr = app.stdscr
        self.height, self.width = self.stdscr.getmaxyx()

        self.win = curses.newwin(self.height, self.width, 0, 0)

        self.monitored_file: LogMonitor = app.file

        self.lines: list[str] = []
        self.scroll_offset = 0
        self.selected_line = 0
        self.follow_mode = True

        self._init_colors()

    def _init_colors(self):

        self.stdscr.nodelay(True)
        self.stdscr.timeout(100)

        curses.start_color()
        curses.use_default_colors()

        # Hide cursor
        curses.curs_set(0)

        # Define color pairs
        curses.init_pair(0, curses.COLOR_WHITE, -1)
        curses.init_pair(1, curses.COLOR_CYAN, -1)
        curses.init_pair(2, curses.COLOR_MAGENTA, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_RED, -1)
        curses.init_pair(5, curses.COLOR_RED, -1)
        curses.init_pair(15, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    def _split_line(self, line: str) -> Optional[LogLine]:
        pattern = r"^(?P<date>\S+ \S+)\s+\[(?P<level>\w+)\]\s+(?P<message>.*)$"
        match = re.match(pattern, line)

        if not match:
            return None

        return LogLine(
            date=match.group("date"),
            level=match.group("level"),
            message=match.group("message"),
        )

    def _draw_header(self):
        self.win.addstr(1, 3, "Time")
        self.win.addstr(1, 18, "Level")
        self.win.addstr(1, 30, "Message")

        self.win.attron(curses.color_pair(15) | curses.A_DIM)
        self.win.hline(2, 1, curses.ACS_HLINE, self.width)
        self.win.box()
        self.win.attroff(curses.color_pair(15) | curses.A_DIM)

        text = self.monitored_file.time_since_last_change()
        last_update = f"Updated: {text}s"

        try:
            self.win.addstr(
                1, self.width - len(last_update)-4, last_update, curses.A_DIM
            )
        except curses.error:
            pass

    def _draw_logfile(self) -> None:
        visible_height = self.height - 4

        visible_lines = self.lines[
            self.scroll_offset: self.scroll_offset + visible_height
        ]

        for i, raw_line in enumerate(visible_lines):
            parsed: Optional[LogLine] = self._split_line(raw_line)
            if not parsed:
                continue

            y: int = i + self.VIEW_TOP
            global_index: int = self.scroll_offset + i

            # Highlight selected line
            if global_index == self.selected_line and not self.follow_mode:
                self.win.addstr(y, 1, ">", curses.color_pair(3))

            # Date
            try:
                self.win.addnstr(
                    y,
                    2,
                    parsed.date[10:],
                    24,
                    curses.color_pair(0) | curses.A_DIM,
                )
            except curses.error:
                pass

            level_key = f"[{parsed.level}]"
            color = self.LOG_COLOR_MAP.get(level_key, 1)

            # Level
            try:
                self.win.addstr(
                    y,
                    18,
                    level_key,
                    curses.color_pair(color),
                )
            except curses.error:
                pass

            # Message
            try:
                self.win.addnstr(
                    y,
                    30,
                    parsed.message,
                    self.width - 34,
                )
            except curses.error:
                pass

    def _draw_indicators(self) -> None:
        visible_height: int = self.height - 4

        has_above: int = self.scroll_offset > 0
        has_below: int = self.scroll_offset + visible_height < len(self.lines)

        self.win.attron(curses.color_pair(15) | curses.A_BOLD)

        try:
            if has_above:
                self.win.addstr(self.VIEW_TOP, self.width - 3, "↑")

            if has_below:
                self.win.addstr(self.height - 2, self.width - 3, "↓")
        except curses.error:
            pass

        self.win.attroff(curses.color_pair(15) | curses.A_DIM)

    def draw(self) -> None:
        self.height, self.width = self.stdscr.getmaxyx()
        self.win.erase()

        self._draw_header()
        self._draw_logfile()
        self._draw_indicators()

        self.win.noutrefresh()

    def update(self) -> None:
        if not self.monitored_file.has_changed():
            return

        new_lines: list[str] = self.monitored_file.read()

        self.lines = new_lines

    def _adjust_offset(self) -> None:
        """Adjust the top-of-window offset to keep the cursor visible."""

        height = self.win.getmaxyx()[0] - 4

        if self.selected_line < self.scroll_offset:
            self.scroll_offset = self.selected_line

        elif self.selected_line >= self.scroll_offset + height:
            self.scroll_offset = self.selected_line - height + 1
