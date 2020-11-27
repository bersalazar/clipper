import os
import logging

from config import config
from tinydb import TinyDB
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def output_as_pdf():
    database_path = config['database_path']
    if not os.path.isfile(database_path):
        logger.error(f'database does not exist at {database_path}')
        exit()

    author_style = ParagraphStyle('source')
    author_style.fontSize = 7
    author_style.textColor = 'grey'
    text_style = ParagraphStyle('text')
    text_style.alignment = TA_JUSTIFY
    text_style.fontSize = 10
    document = [Spacer(1, 1)]
    for quote in TinyDB(database_path):
        document.append(Paragraph(f'{quote["text"]}', text_style))
        document.append(Paragraph(f'{quote["author"]} in {quote["book"]} '
                                  '[{quote.doc_id}]', author_style))
        document.append(Spacer(1, 10))

    pdf_output_path = config['pdf_output_path']
    doc = SimpleDocTemplate(pdf_output_path, pagesize=letter)
    doc.build(document)
    logger.info(f'Successfully created {pdf_output_path}')


def output_text_file():
    output_file = config['new_clippings_file']
    logger.info(f'Outputing to {output_file}')
    if os.path.isfile(output_file):
        os.remove(output_file)

    db = TinyDB('./db.json')

    f = open(output_file, 'a')
    for clipping in db:
        for line in clipping['block']:
            f.write(line)
        f.write('==========\n')
    f.close()

    logger.info(f'Succesfully output to {output_file}')
