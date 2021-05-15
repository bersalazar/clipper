from argparse import ArgumentParser

import services.clip as clip
import services.clean as clean
import services.output as output
from logger import logger

arg_parser = ArgumentParser()


def get_args():
    subparsers = arg_parser.add_subparsers(dest='subcommand', help='sub-command help')

    parser_clip = subparsers.add_parser('clip', help='goes through the file and clips quotes')
    parser_clip.add_argument('--file', help='the file to clip', required=True)

    parser_clean = subparsers.add_parser('clean', help='cleans the clips db')
    parser_clean.add_argument('--key', nargs='?', help='the key of the clip')
    parser_clean.add_argument('--list', help='the file holding a list of keys of clips to clean')

    parser_output = subparsers.add_parser('output', help='creates an output file of the clippings database')
    parser_output.add_argument('--text', action='store_true', help='in a kindle clippings text file')
    parser_output.add_argument('--pdf', action='store_true', help='in a pdf file')
    parser_output.add_argument('--starred', nargs='?', help='starred quotes from a file in a pdf file')

    parser_clip = subparsers.add_parser('fetch', help='fetch the My Clippings.txt file from kindle')

    return arg_parser.parse_args()


def main():
    args = get_args()

    if not args.subcommand:
        arg_parser.print_help()

    if args.subcommand == 'clean':
        if args.key:
            clean.by_key(args)
        elif args.list:
            logger.info("this is not working well because the indexes have changed after cleanup")
            # clean_by_list(args.list)
        else:
            clean.duplicates()

    elif args.subcommand == 'output':
        if args.text:
            output.text_file()
        elif args.starred:
            output.starred_as_pdf()
        else:
            output.as_pdf()

    elif args.subcommand == 'clip':
        clip.process(args.file)

    elif args.subcommand == 'fetch':
        logger.info("copying from Kindle: My Clippings.txt file")
        # TODO: copy from the usual directory where My Clippings.txt file resides


if __name__ == '__main__':
    main()
