"""This module provides the CLI for the wrangle-ukds-trade-directories app."""

from . import __app_name__
import argparse
from pathlib import Path


def typecast_args(args):
    args.input = Path(args.input)
    args.output = Path(args.output)

    return args


def test_args(args):
    if not Path(args.input).is_dir():
        raise RuntimeError("The path specified does not exist")

    Path(args.output).mkdir(parents=True, exist_ok=True)

    if not Path(args.output).is_dir():
        raise RuntimeError("The output path specified does not exist")

    return True


def get_args():
    # Create the parser
    p = argparse.ArgumentParser(
        prog=__app_name__, description="Wrangle the UKDS Trade Directories data folder."
    )

    # Add the arguments
    p.add_argument(
        "input",
        metavar="input",
        type=str,
        help="The input path where the UKDS trade directories can be found.",
    )

    p.add_argument(
        "output",
        metavar="output",
        type=str,
        help="The output path where the consolidated UKDS trade directories should be located.",
    )

    # Execute the parse_args() method
    args = p.parse_args()

    # Set types
    args = typecast_args(args)

    # Test args
    test_args(args)

    return args
