"""
@file:    log_viewer.py
@author:  Rob Pellegrin
@date:    04/10/2026

@updated: 04/10/2026

"""

import curses

from app.viewer import LogViewer
from utils.input_handler import InputHandler


class App:

    def __init__(self, file, stdscr: curses.window) -> None:
        self.stdscr = stdscr
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
            curses.doupdate()
