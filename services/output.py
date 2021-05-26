from config import config
from logger import logger
from model import Db
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY


db = Db(
    host=config["db_host"],
    port=config["db_port"],
    database=config["db_name"],
    user=config['db_user'],
    password=config['db_password']
)


def as_pdf():
    author_style = ParagraphStyle('source')
    author_style.fontSize = 7
    author_style.textColor = 'grey'
    text_style = ParagraphStyle('text')
    text_style.alignment = TA_JUSTIFY
    text_style.fontSize = 10
    document = [Spacer(1, 1)]

    sql = 'SELECT QuoteId, BookId, AuthorId, Text FROM Quote'
    quotes = db.query(sql)

    for quote in quotes:
        book_name_sql = f'SELECT Name FROM Book WHERE BookId = {quote[1]}'
        author_sql = f'SELECT Name FROM Author WHERE AuthorId = {quote[2]}'

        book_name = db.query(book_name_sql)[0][0]
        author_name = db.query(author_sql)[0][0]

        document.append(Paragraph(f'{quote[3]}', text_style))
        document.append(Paragraph(f'{author_name} in {book_name} '
                                  f'[{quote[0]}]', author_style))
        document.append(Spacer(1, 10))

        pdf_output_path = config['pdf_output_path']

    doc = SimpleDocTemplate(pdf_output_path, pagesize=letter)
    doc.build(document)
    logger.info(f'Successfully created {pdf_output_path}')
