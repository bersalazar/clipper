import os
import argparse
from model import Quote, logger
from tinydb import TinyDB, Query, where

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--source', '-s', help='path to the source db', default='./db.json')
args = arg_parser.parse_args()

db_path = './db.json'
db = TinyDB(db_path)

previous_quote = ''
duplicates = []
for quote in TinyDB(args.source):
    if quote['text'].startswith(previous_quote[:25]):
        duplicates.append(quote.doc_id-1)
    previous_quote = quote['text']

duplicates.pop(0)
db.remove(doc_ids=duplicates)
logger.info(f'Removed {len(duplicates)} duplicate records')