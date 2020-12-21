import os
import logging

from config import config
from tinydb import TinyDB, where
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def check_database_path():
    database_path = config['database_path']
    if not os.path.isfile(database_path):
        logger.error(f'database does not exist at {database_path}')
        exit()


def output_starred_as_pdf():
    check_database_path()
    db = TinyDB(config['database_path'])

    f = open('./files/starred_quotes', 'r', encoding='utf-8-sig')
    starred_quotes = []

    for line in f:
        try:
            key = int(line)
            print(db.get(doc_id=key))
            starred_quotes.append(db.get(doc_id=key))
        except KeyError as ex:
            logger.error('The specified key was not found', ex)

    author_style = ParagraphStyle('source')
    author_style.fontSize = 7
    author_style.textColor = 'grey'
    text_style = ParagraphStyle('text')
    text_style.alignment = TA_JUSTIFY
    text_style.fontSize = 10
    document = [Spacer(1, 1)]
    for quote in starred_quotes:
        document.append(Paragraph(f'{quote["text"]}', text_style))
        document.append(Paragraph(f'{quote["author"]} in {quote["book"]} '
                                  f'[{quote.doc_id}]', author_style))
        document.append(Spacer(1, 10))

    output_path = config['starred_pdf_output_path']
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    doc.build(document)
    logger.info(f'Successfully created {output_path}')


def output_as_pdf():
    check_database_path()
    author_style = ParagraphStyle('source')
    author_style.fontSize = 7
    author_style.textColor = 'grey'
    text_style = ParagraphStyle('text')
    text_style.alignment = TA_JUSTIFY
    text_style.fontSize = 10
    document = [Spacer(1, 1)]
    for quote in TinyDB(config['database_path']):
        document.append(Paragraph(f'{quote["text"]}', text_style))
        document.append(Paragraph(f'{quote["author"]} in {quote["book"]} '
                                  f'[{quote.doc_id}]', author_style))
        document.append(Spacer(1, 10))

    pdf_output_path = config['pdf_output_path']
    doc = SimpleDocTemplate(pdf_output_path, pagesize=letter)
    doc.build(document)
    logger.info(f'Successfully created {pdf_output_path}')


def output_text_file():
    output_file = config['new_clippings_file']
    logger.info(f'Outputting to {output_file}')
    if os.path.isfile(output_file):
        os.remove(output_file)

    db = TinyDB(config['database_path'])

    f = open(output_file, 'a')
    for clipping in db:
        for line in clipping['block']:
            f.write(line)
        f.write('==========\n')
    f.close()

    logger.info(f'Succesfully output to {output_file}')
