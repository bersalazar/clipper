import os
import argparse
import logging
from model import Quote
from tinydb import TinyDB, Query

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--output', '-o', help='output file name', default='./quotes.pdf')
arg_parser.add_argument('--source', '-s', help='path to the source db', default='./db.json')
arg_parser.add_argument('--txt', '-t', action="store_true", help='output as a My Clippings.txt file', default=False)
args = arg_parser.parse_args()

if (not args.txt):
    if not os.path.isfile(args.source):
        logger.error(f'database does not exist at {args.source}')
        exit() 

    author_style = ParagraphStyle('source')
    author_style.fontSize = 7
    author_style.textColor = 'grey'
    text_style = ParagraphStyle('text')
    text_style.alignment=TA_JUSTIFY
    text_style.fontSize = 10
    previous_book = ''
    document = [Spacer(1,1)]
    for quote in TinyDB(args.source):
        document.append(Paragraph(f"{quote['text']}", text_style))
        document.append(Paragraph(f"{quote['author']} in {quote['book']} [{quote.doc_id}]", author_style))
        document.append(Spacer(1, 10))
        previous_book = quote['book']

    doc = SimpleDocTemplate(args.output, pagesize=letter)
    doc.build(document)
    logger.info(f'Successfully created {args.output}')
else:
    output_file = './new_clippings.txt' 
    if os.path.isfile(output_file):
        os.remove(output_file) 

    db = TinyDB('./db.json')
    blocks = []

    f = open(output_file, "a")
    for clipping in db:
        for line in clipping['block']:
            f.write(line)
        f.write('==========\n')
    f.close()
