import argparse
from pathlib import Path
from .formatter import CustomHelpFormatter
import logging


def build_parser():

    parser = argparse.ArgumentParser(
        prog="pyrepgen",
        description="Generate reports from GitLab/GitHub repositories for verification reports.",
        formatter_class=CustomHelpFormatter,
        #epilog="TODO",
    )

    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        required=False,
        metavar="MODE",
        default="normal",
        choices=["normal", "read"],
        help="Operation mode (choices: normal, read) [default: normal]",
    )

    parser.add_argument(
        "-t",
        "--tool",
        type=str,
        required=False,
        metavar="TOOL",
        default="gitlab",
        choices=["gitlab", "github"],
        help="Version control tool (choices: gitlab, github) [default: gitlab]",
    )

    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        required=True,
        metavar="FILE",
        help="YAML configuration file path",
    )

    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=False,
        metavar="FILE",
        help="Input JSON file path",
    )

    args = parser.parse_args()
    
    # Validate yaml file
    if  not args.config.exists():
        parser.error(f"Input YAML file {args.config} does not exist")

    # Validate arguments read mode
    if args.mode == "read" and not args.input:
        parser.error("Input JSON file must be specified in read mode")
    
    if args.mode == "read" and not args.input.exists():
        parser.error(f"Input JSON file {args.input} does not exist")

    return parser
