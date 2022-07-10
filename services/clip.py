from logger import logger
from model import Quote, Db
from config import config

db = Db(
    host=config["db_host"],
    port=config["db_port"],
    database=config["db_name"],
    user=config["db_user"],
    password=config["db_password"],
)

# Indicates how many characters from a quote should be evaluated before considering it a duplicate
duplicate_search_substring_threshold = config["duplicate_search_substring_threshold"]


def read_file(path):
    block = []
    clips = []

    f = open(path, "r", encoding="utf-8-sig")
    for line in f:
        if line.startswith("="):
            clips.append(block)
            block = []
        else:
            block.append(line)
    f.close()
    return clips


def process_clippings_file(path):
    quotes = []
    clips = read_file(path)

    for clip in clips:
        quotes.append(Quote.from_block(clip))
    logger.info(f"Parsed {len(clips)} quotes from {path}")

    return quotes


def remove_duplicates(quotes):
    unique_quotes = []
    for quote in quotes:
        print(quote.text)

    return unique_quotes


def insert_author(author):
    max_id_sql = "SELECT max(AuthorId) FROM Author"
    result = db.query(max_id_sql)

    author_id = int(result[0][0]) + 1
    db.query(f'INSERT INTO Author (AuthorId, Name) VALUES ({author_id}, "{author}")')

    return author_id


def get_author_id(author):
    sql = f'SELECT AuthorId FROM Author WHERE Name="{author}"'
    result = db.query(sql)

    if result:
        author_id = int(result[0][0])
        logger.info(f"Found author ID for {author}: {author_id}")
        return author_id

    return insert_author(author)


def insert_book(book, author_id):
    sql = "SELECT max(BookId) FROM Book"
    result = db.query(sql)

    book_id = int(result[0][0]) + 1
    db.query(f'INSERT INTO Book (Name, AuthorId) VALUES ("{book}", {author_id})')

    return book_id


def get_book_id(book, author):
    sql = f'SELECT BookId FROM Book WHERE Name="{book}"'
    result = db.query(sql)

    if result:
        book_id = int(result[0][0])
        logger.info(f"Found book ID for {book}: {book_id}")
        return book_id

    return insert_book(book, author)


def clean_quote_text(text):
    text = text.strip()
    text = add_quote_character_escape(text)

    return text


def insert_quote(author_id, book_id, quote, to_temporary_table=False):
    table = "Temporary" if to_temporary_table else "Quote"
    text = clean_quote_text(quote.text)
    db.query(
        f"""
        INSERT INTO {table} (Text, DateAdded, Page, Location, BookId, AuthorId)
        VALUES ("{text}", "{quote.date}", "{quote.page}", "{quote.location}", {book_id}, {author_id})
    """
    )


def add_quote_character_escape(text):
    if "'" in text:
        text = text.replace("'", "\\'")
    if '"' in text:
        text = text.replace('"', '\\"')
    return text


def get_unique_quote(quote):
    """
    Searches Temporary table for quote duplicates and returns the valid, unique quote, which is the one with the MAX rown number.
    """
    search_substring = quote.text[:duplicate_search_substring_threshold]
    search_substring = clean_quote_text(search_substring)
    sql = f"""
    WITH temp AS
    (
        SELECT *, row_number() over (order by QuoteId) RowNumber
        FROM Temporary
        WHERE Text LIKE \"%{search_substring}%\"
    )
    SELECT *
    FROM temp
    WHERE RowNumber = (SELECT max(RowNumber) FROM temp)
    """

    result = db.query(sql)
    if result:
        result_tuple = result[0]
        return Quote(
            text=result_tuple[1],
            date=result_tuple[2],
            page=result_tuple[3],
            location=result_tuple[4],
            book_id=result_tuple[5],
            author_id=result_tuple[6],
        )
    return quote


def is_duplicate_quote(quote):
    clean_text = clean_quote_text(quote.text)
    sql = f'SELECT QuoteId FROM Quote WHERE Text="{clean_text}"'
    result = db.query(sql)

    if result:
        logger.warning(f"DUPLICATE FOUND: {quote.text}")
        return True
    return False


def clip(path):
    quotes = process_clippings_file(path)
    print(quotes[22].as_json())
