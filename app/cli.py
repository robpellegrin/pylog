"""
@file:    cli.py
@author:  Rob Pellegrin
@date:    03-24-2026

@updated: 03-24-2026

"""

import argparse


def process_args() -> argparse.ArgumentParser.parse_args:
    parser = argparse.ArgumentParser(description="Process a file")
    parser.add_argument('file', help="Path to log file")

    return parser.parse_args()
