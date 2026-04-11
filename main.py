"""
@file:    main.py
@author:  Rob Pellegrin
@date:    03/23/2026

@updated: 04/10/2026

"""

import curses
import logging
from pathlib import Path

from app.app import App
from app.cli import process_args
from utils.file_monitor import FileMonitor


def main(stdscr: curses.window) -> None:
    args = process_args()

    file = FileMonitor(Path(args.file))

    # win = LogViewer(stdscr=stdscr, file=file)
    # win.run()

    app = App(file, stdscr)
    app.run()


if __name__ == '__main__':
    # Setup logging.
    logfile = Path(__file__).name
    logging.basicConfig(
        filename=f"logs/{logfile}.log",
        level=logging.NOTSET,
        filemode='w',
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
