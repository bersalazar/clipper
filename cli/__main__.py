from argparse import ArgumentParser
from logger import logger

from config import config
from .clip_service import process_clippings
from .clean_service import clean_by_key, clean_by_list, clean_duplicates
from .output_service import output_text_file, output_as_pdf


def get_args():
    arg_parser = ArgumentParser(epilog='Example usage: ')
    subparsers = arg_parser.add_subparsers(dest='subcommand',
                                           help='sub-command help')

    parser_clean = subparsers.add_parser('clean', help='cleans the clips db')
    parser_clean.add_argument('--key', nargs='?', help='the key of the clip')
    parser_clean.add_argument('--list', nargs='?', help='a list of keys of clips')

    parser_clip = subparsers.add_parser('clip', help='goes through the file and clips quotes')
    parser_clip.add_argument('--file', help='the file to clip')

    parser_output = subparsers.add_parser('output', help='creates an output file of the clippings database')
    parser_output.add_argument('--text', action='store_true', help='in a kindle clippings text file')
    parser_output.add_argument('--pdf', action='store_true', help='in a pdf file')

    return arg_parser.parse_args()


def main():
    args = get_args()

    print(f'Using {config.get("database_path")} database')
    if args.subcommand == 'clean':
        if args.key:
            logger.info("CLEAN!")
            clean_by_key(args)
        elif args.list:
            logger.info("BY LIST!")
            clean_by_list(args)
        else:
            logger.info("BY DUPES")
            clean_duplicates()
    elif args.subcommand == 'output':
        if args.text:
            logger.info("TEXT!")
            output_text_file()
        elif args.pdf:
            logger.info("PDF")
            output_as_pdf()
    elif args.subcommand == 'clip':
        if args.file:
            logger.info('clipping the file')
            process_clippings(args.file)


if __name__ == '__main__':
    main()
