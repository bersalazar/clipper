import logging
import sys
from argparse import ArgumentParser
from .clip import process_clippings
from .clean import *
from config import *

def get_args():
    arg_parser = ArgumentParser(epilog='Example usage: ')
    #arg_parser.add_argument('--path', '-p', help='the path to the clippings file')
    arg_parser.add_argument('--clean', '-c', help='the path to the clippings file')
    arg_parser.add_argument('--key', '-k', help='clean a single quote by its ID')
    args = arg_parser.parse_args()
    return args

def main():
    args = get_args()
    logging.basicConfig(level=logging.INFO)
    print(f'Using {config.get("database_path")} database')
    #args = sys.argv[1:]

    print(args)
    if args.clean:
        clean(args)
        print("CLEAN!")


if __name__ == '__main__':
    main()
