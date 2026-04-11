"""
@file:    main.py
@author:  Rob Pellegrin
@date:    03-23-2026

@updated: 04-10-2026

"""

import curses
import logging
from pathlib import Path

from cursedlog.cli import process_args
from cursedlog.core import App
from cursedlog.monitor import LogMonitor


def main(stdscr: curses.window) -> None:
    args = process_args()

    file = LogMonitor(Path(args.file))

    app = App(file, stdscr)
    app.run()


if __name__ == "__main__":
    logfile = Path(__file__)
    Path("logs").mkdir(exist_ok=True)

    # Setup logging.
    logging.basicConfig(
        filename=f"logs/{logfile.stem}.log",
        level=logging.INFO,
        filemode="w",
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
