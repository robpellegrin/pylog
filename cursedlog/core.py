"""
@file:    core.py
@author:  Rob Pellegrin
@date:    04/10/2026

@updated: 04/10/2026

"""

import curses

from cursedlog.input import InputHandler
from cursedlog.viewer import LogViewer


class App:

    def __init__(self, file, stdscr: curses.window) -> None:
        self.stdscr = stdscr
        self.stdscr.nodelay(True)
        self.stdscr.timeout(100)

        self._init_colors()

        self.follow_mode = True
        self.input_handler = InputHandler(self)
        self.file = file
        self.window = LogViewer(self)

    def run(self) -> None:
        while True:
            self.input_handler.handle_input()
            self.window.update()

            if self.follow_mode:
                view_height = self.window.height - 4
                self.window.scroll_offset = max(
                    0, len(self.window.lines) - view_height
                )
                self.window.selected_line = max(0, len(self.window.lines) - 1)

            self.window.draw()

    def _init_colors(self):
        curses.start_color()
        curses.use_default_colors()

        # Hide cursor
        curses.curs_set(False)

        # Define color pairs
        curses.init_pair(0, curses.COLOR_WHITE, -1)
        curses.init_pair(1, curses.COLOR_CYAN, -1)
        curses.init_pair(2, curses.COLOR_MAGENTA, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_RED, -1)
        curses.init_pair(5, curses.COLOR_RED, -1)
        curses.init_pair(15, curses.COLOR_MAGENTA, -1)
