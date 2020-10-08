import os
import argparse
from model import Quote, logger
from tinydb import TinyDB, Query

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--path', help='path to the Kindle clippings file', default='My Clippings.txt', required=False)
arg_parser.add_argument('--output', help='output type [json, pdf]', default='pdf', required=False)
args = arg_parser.parse_args()

block = []
clips = []

# if arg is parse then parse and generate db.json
f = open(args.path, 'r', encoding='utf-8-sig')
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

logger.info("Inserting records to the db...")
db.insert_multiple({
    'book': quote.book, 
    'author': quote.author,
    'text': quote.text,
    'block': quote.block
} for quote in quotes)

# if arg is print then read db.json and generate pdf
# should use dynamodb or a hosted mongo or small doc based db and not store locally, this way I can generate more functions to analyze, remove duplicates, do diffs. Do some better quote management
document = []
for quote in db:
    document.append(Paragraph(f"{quote['book']} by {quote['author']}", ParagraphStyle('bold')))
    document.append(Paragraph(quote['text']))
    document.append(Spacer(1, 20))

SimpleDocTemplate('quotes.pdf', pagesize=letter).build(document)