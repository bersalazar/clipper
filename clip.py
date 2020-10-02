import os
from model import Quote, logger
from tinydb import TinyDB, Query

block = []
clips = []
f = open('My Clippings.txt', 'r', encoding='utf-8-sig')
for line in f:
    if line.startswith('='):
        clips.append(block)
        block = []
    else:
        block.append(line)

f.close()

# db
db_path = './db.json'
if os.path.isfile(db_path):
    os.remove('./db.json') 
db = TinyDB(db_path)

quotes = []
for clip in clips:
    quote = Quote(clip)
    quotes.append(quote)
    logger.info(f'Added quote for book: {quote.book}; author: {quote.author}')

logger.info("Inserting records to the db...")
db.insert_multiple({
    'book': quote.book, 
    'author': quote.author,
    'text': quote.text
} for quote in quotes)