import os

from tinydb import TinyDB

from logger import logger
from model import Quote
from config import config

db_path = config['database_path']


def read_file(path):
    block = []
    clips = []

    f = open(path, 'r', encoding='utf-8-sig')
    for line in f:
        if line.startswith('='):
            clips.append(block)
            block = []
        else:
            block.append(line)
    f.close()
    return clips


def process(path):
    if os.path.isfile(db_path):
        os.remove(db_path)
    db = TinyDB(db_path)

    quotes = []
    clips = read_file(path)

    for clip in clips:
        quotes.append(Quote(clip))
    logger.info(f"Parsed {len(clips)} quotes from {path}")

    db.insert_multiple({
        'book': quote.book,
        'author': quote.author,
        'text': quote.text,
        'block': quote.block
    } for quote in quotes)
    logger.info("Inserted all records to the db")
    db.close()
