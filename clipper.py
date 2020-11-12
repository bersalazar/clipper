import logging
from argparse import ArgumentParser
from clip import process_clippings

def get_args():
    arg_parser = ArgumentParser(epilog='Example usage: ')
    arg_parser.add_argument('--path', '-p', help='the path to the clippings file', default='My Clippings.txt')
    args = arg_parser.parse_args()
    return args

def main():
    args = get_args()
    logging.basicConfig(level=logging.INFO)

    if args.path:
        process_clippings(args.path)

if __name__ == '__main__':
    main()
