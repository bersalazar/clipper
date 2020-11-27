import os
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

def output_as_pdf(args):
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


def output_text_file():
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
