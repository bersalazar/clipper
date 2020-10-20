import os
import argparse
from model import Quote, logger
from tinydb import TinyDB, Query, where
from config import config

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--key', '-k', help='clean a single quote by its ID')
args = arg_parser.parse_args()

db_path = config['database_path']
db = TinyDB(db_path)

if args.key:
    try:
        db.remove(doc_ids=[int(args.key)])
        logger.info(f'Removed quote with ID {args.key}')
    except KeyError as ex:
        logger.error('The specified key was not found', ex)
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
