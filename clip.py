import os
import argparse
from model import Quote, logger
from tinydb import TinyDB, Query

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--path', '-p', help='the path to the clippings file', default='My Clippings.txt')
args = arg_parser.parse_args()

block = []
clips = []

f = open(args.path, 'r', encoding='utf-8-sig')
for line in f:
    if line.startswith('='):
        clips.append(block)
        block = []
    else:
        block.append(line)
f.close()

db_path = './db.json'
if os.path.isfile(db_path):
    os.remove('./db.json') 
db = TinyDB(db_path)

quotes = []
for clip in clips:
    quotes.append(Quote(clip))
logger.info("Parsed quotes from clippings")

db.insert_multiple({
    'book': quote.book, 
    'author': quote.author,
    'text': quote.text,
    'block': quote.block
} for quote in quotes)
logger.info("Inserted all records to the db")
