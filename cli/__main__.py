from argparse import ArgumentParser
from logger import logger

from config import config
from .clip_service import process_clippings
from .clean_service import clean_by_key, clean_by_list, clean_duplicates
from .output_service import output_text_file, output_as_pdf, output_starred_as_pdf


def get_args():
    arg_parser = ArgumentParser(epilog='Example usage: ')
    subparsers = arg_parser.add_subparsers(dest='subcommand', help='sub-command help')

    parser_clean = subparsers.add_parser('clean', help='cleans the clips db')
    parser_clean.add_argument('--key', nargs='?', help='the key of the clip')
    parser_clean.add_argument('--list', help='the file holding a list of keys of clips to clean')

    parser_clip = subparsers.add_parser('clip', help='goes through the file and clips quotes')
    parser_clip.add_argument('--file', help='the file to clip')

    parser_output = subparsers.add_parser('output', help='creates an output file of the clippings database')
    parser_output.add_argument('--text', action='store_true', help='in a kindle clippings text file')
    parser_output.add_argument('--pdf', action='store_true', help='in a pdf file')
    parser_output.add_argument('--starred', nargs='?', help='starred quotes from a file in a pdf file')

    parser_clip = subparsers.add_parser('fetch', help='fetch the My Clippings.txt file from kindle')

    return arg_parser.parse_args()


def print_usage():
    print("usage")


def main():
    args = get_args()

    if args.subcommand not in ['clean', 'output', 'clip', 'fetch']:
        print_usage()
        exit(0)

    print(f'Using {config.get("database_path")} database')
    if args.subcommand == 'clean':
        if args.key:
            clean_by_key(args)
        elif args.list:
            logger.info("this is not working well because the indexes have changed after cleanup")
            # clean_by_list(args.list)
        else:
            clean_duplicates()

    elif args.subcommand == 'output':
        if args.text:
            output_text_file()
        elif args.pdf:
            output_as_pdf()
        elif args.starred:
            output_starred_as_pdf()

    elif args.subcommand == 'clip':
        if not args.file:
            logger.error("A file needs to be specified")
            print_usage()

        process_clippings(args.file)
        clean_duplicates()

    elif args.subcommand == 'fetch':
        logger.info("copying from Kindle: My Clippings.txt file")


if __name__ == '__main__':
    main()
