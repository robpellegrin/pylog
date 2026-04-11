"""
@file:    input.py
@author:  Rob Pellegrin
@date:    04/10/2026

@updated: 04/10/2026

"""


import curses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app import App


class InputHandler:
    def __init__(self, app: "App") -> None:
        self.app = app

    def handle_input(self) -> None:
        try:
            key: int = self.app.stdscr.getch()
        except curses.error:
            return

        if key == ord("q"):
            raise KeyboardInterrupt

#        view_height = self.height - 4
#        max_offset = max(0, len(self.lines) - view_height)
#
#        if key in (ord("j"), curses.KEY_DOWN):
#            self.selected_line = min(
#                self.selected_line + 1, len(self.lines) - 1)
#            self._adjust_offset()
#            self.follow_mode = False
#
#        elif key == curses.KEY_ENTER:
#            # Display full log entry in subwindow.
#            pass
#
#        elif key == curses.KEY_F5:
#            # Display filter window.
#            pass
#
#        elif key in (ord("k"), curses.KEY_UP):
#            self.selected_line = max(self.selected_line - 1, 0)
#            self._adjust_offset()
#            self.follow_mode = False
#
#        elif key == curses.KEY_NPAGE:
#            self.scroll_offset = min(
#                self.scroll_offset + view_height, max_offset
#            )
#            self.follow_mode = False
#
#        elif key == curses.KEY_PPAGE:
#            self.scroll_offset = max(self.scroll_offset - view_height, 0)
#            self.follow_mode = False
#
#        elif key == ord("G"):
#            self.scroll_offset = max_offset
#            self.follow_mode = True
#
#        elif key == curses.KEY_RESIZE:
#            self.update()
#
#        elif key == ord("f"):
#            self.follow_mode = not self.follow_mode
