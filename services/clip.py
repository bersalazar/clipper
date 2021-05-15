from logger import logger
from model import Quote, Db
from exceptions import QuoteAlreadExistsException
from config import config

db = Db(
    host=config["db_host"],
    port=config["db_port"],
    database=config["db_name"],
    user=config['db_user'],
    password=config['db_password']
)


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


def parse_clippings_file(path):
    quotes = []
    clips = read_file(path)

    for clip in clips:
        quotes.append(Quote(clip))
    logger.info(f"Parsed {len(clips)} quotes from {path}")

    return quotes


def insert_author(author):
    max_id_sql = "SELECT max(AuthorId) FROM kindle.Author"
    result = db.query(max_id_sql)

    author_id = int(result[0][0])+1
    db.query(f'INSERT INTO kindle.Author (AuthorId, Name) VALUES ({author_id}, "{author}")')

    return author_id


def get_author_id(author):
    sql = f'SELECT AuthorId FROM kindle.Author WHERE Name="{author}"'
    result = db.query(sql)

    if result:
        author_id = int(result[0][0])
        logger.info(f"Found author ID for {author}: {author_id}")
        return author_id

    return insert_author(author)


def insert_book(book, author_id):
    sql = "SELECT max(BookId) FROM kindle.Book"
    result = db.query(sql)

    book_id = int(result[0][0])+1
    db.query(f'INSERT INTO kindle.Book (Name, AuthorId) VALUES ("{book}", {author_id})')

    return book_id


def get_book_id(book, author):
    sql = f'SELECT BookId FROM kindle.Book WHERE Name="{book}"'
    result = db.query(sql)

    if result:
        book_id = int(result[0][0])
        logger.info(f"Found book ID for {book}: {book_id}")
        return book_id

    return insert_book(book, author)


def clean_quote_text(text):
    text = text.strip()
    text = text.replace("\"", "")

    return text


def insert_quote(author_id, book_id, quote):
    text = clean_quote_text(quote.text)
    sql = f'SELECT QuoteId FROM kindle.Quote WHERE Text="{text}"'
    result = db.query(sql)

    if result:
        raise QuoteAlreadExistsException()

    db.query(f'''
    INSERT INTO kindle.Quote (Text, DateAdded, Page, Location, BookId, AuthorId)
    VALUES ("{text}", "{quote.date}", "{quote.page}", "{quote.location}", {book_id}, {author_id})
    ''')


def process(path):
    quotes = parse_clippings_file(path)

    for quote in quotes:
        author_id = get_author_id(quote.author)
        book_id = get_book_id(quote.book, author_id)
        try:
            insert_quote(author_id, book_id, quote)
        except QuoteAlreadExistsException:
            logger.warning("Quote already exists. Skipping...")

    logger.info("Inserted records to the DB")
