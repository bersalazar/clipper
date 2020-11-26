import logging
import sys
from argparse import ArgumentParser
from .clip import process_clippings
from .clean import *
from config import *

def get_args():
    arg_parser = ArgumentParser(epilog='Example usage: ')
    subparsers = arg_parser.add_subparsers(help='sub-command help')

    parser_clean = subparsers.add_parser('clean', help='cleans the clips db')
    parser_clean.add_argument('key', help='the key of the clip')
    
    parser_clip = subparsers.add_parser('clip', help='goes through the file and clips quotes')
    parser_clip.add_argument('file', help='the file to clip')

    return arg_parser.parse_args()

def main():
    args = get_args()
    logging.basicConfig(level=logging.INFO)

    print(f'Using {config.get("database_path")} database')

    if args.key:
        clean(args)
        print("CLEAN!")


if __name__ == '__main__':
    main()
