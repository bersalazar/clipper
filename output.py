import os
import argparse
from model import Quote, logger
from tinydb import TinyDB, Query

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--output', '-o', help='output file name', default='./quotes.pdf')
arg_parser.add_argument('--source', '-s', help='path to the source db', default='./db.json')
args = arg_parser.parse_args()

document = []
if not os.path.isfile(args.source):
    logger.error(f'database does not exist at {args.source}')
    exit() 

for quote in TinyDB(args.source):
    document.append(Paragraph(f"{quote['book']} by {quote['author']}", ParagraphStyle('bold')))
    document.append(Paragraph(quote['text']))
    document.append(Spacer(1, 20))

SimpleDocTemplate(args.output, pagesize=letter).build(document)
