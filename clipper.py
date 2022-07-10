from argparse import ArgumentParser

import services.clip as clip
import services.clean as clean
import services.output as output
from logger import logger

arg_parser = ArgumentParser()


def get_args():
    subparsers = arg_parser.add_subparsers(dest="subcommand", help="sub-command help")

    parser_clip = subparsers.add_parser(
        "clip", help="Reads the specified file and clips quotes"
    )
    parser_clip.add_argument(
        "--file",
        help="Path to the local file to clip",
        nargs="?",
        default="files/My Clippings.txt",
    )

    parser_clean = subparsers.add_parser(
        "clean", help="Cleans the clips DB. Default is to clean duplicates"
    )
    parser_clean.add_argument("--key", nargs="?", help="ID of the quote to clean")
    parser_clean.add_argument(
        "--list", help="Path to the file holding a list of quote IDs to clean"
    )

    parser_output = subparsers.add_parser(
        "output", help="Creates an readable PDF file of the quotes database"
    )
    parser_output.add_argument(
        "--titles", nargs="?", help="List of IDs of book titles to output"
    )

    parser_clip = subparsers.add_parser(
        "fetch",
        help="TODO: Fetch the My Clippings.txt file from kindle and store it in files/. It also creates a backup copy of the existing one.",
    )

    return arg_parser.parse_args()


def main():
    args = get_args()

    if not args.subcommand:
        arg_parser.print_help()
    if args.subcommand == "clean":
        if args.key:
            clean.by_key(args)
        elif args.list:
            clean.by_list(args.list)
        else:
            clean.duplicates()
    elif args.subcommand == "output":
        if args.titles:
            print("By titles" + args.title)
            output.by_titles(args.titles)
        else:
            output.all()
    elif args.subcommand == "clip":
        clip.clip(args.file)
    elif args.subcommand == "fetch":
        logger.info("TODO: copying from Kindle: My Clippings.txt file")
        # TODO: copy from the usual directory where My Clippings.txt file resides
