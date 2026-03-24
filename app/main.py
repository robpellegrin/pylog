"""
@file:    main.py
@author:  Rob Pellegrin
@date:    03-23-2026

@updated: 03-23-2026

"""

import curses
import logging
from pathlib import Path

from monitor import FileMonitor
from viewer import LogViewer


def main(stdscr: curses.window) -> None:
    logfile = f"{__file__}.log"

    # Setup logging.
    logging.basicConfig(
        filename=logfile,
        level=logging.NOTSET,
        filemode='w',
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    # log.info("Calling main")
    file = FileMonitor(Path("../test.log"))

    win = LogViewer(stdscr=stdscr, file=file)
    win.run()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
