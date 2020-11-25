import os
#import argparse
import logging
from model import Quote
from tinydb import TinyDB, Query, where
from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

#arg_parser = argparse.ArgumentParser()
#arg_parser.add_argument('--key', '-k', help='clean a single quote by its ID')
#arg_parser.add_argument('--list', '-l', help='clean quotes based on IDs in a file')
#args = arg_parser.parse_args()

db_path = config['database_path']
db = TinyDB(db_path)

def clean(args):
    if args.key:
        try:
            db.remove(doc_ids=[int(args.key)])
            logger.info(f'Removed quote with ID {args.key}')
        except KeyError as ex:
            logger.error('The specified key was not found', ex)
    elif args.list:
        f = open(args.list, 'r', encoding='utf-8-sig')
        for line in f:
            try:
                key = int(line)
                db.remove(doc_ids=[key])
                logger.info(f'Removed {key}')
            except KeyError as ex:
                logger.error(f'Key {ex} was not found ')
        f.close()
    else:
        previous_quote = ''
        duplicates = []
        for quote in db:
            if quote['text'].startswith(previous_quote[:25]):
                duplicates.append(quote.doc_id-1)
            previous_quote = quote['text']
        duplicates.pop(0)
        db.remove(doc_ids=duplicates)
        logger.info(f'Removed {len(duplicates)} duplicate records')
