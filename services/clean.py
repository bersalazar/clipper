import re

from logger import logger
from config import config
from model import Db

db = Db(
    host=config["db_host"],
    port=config["db_port"],
    database=config["db_name"],
    user=config['db_user'],
    password=config['db_password']
)

# Indicates how many characters from a quote should be evaluated before considering it a duplicate
duplicate_threshold = 25


def is_valid_quote_id(quote_id):
    regex = re.compile(r'[1-9]+|[1-9]+[0-9]+')
    return True if regex.search(quote_id) else False
    return False


def by_key(args):
    quote_id = args.key

    if not is_valid_quote_id(quote_id):
        raise KeyError(f'{quote_id} is not a valid key')

    try:
        db.query(f'DELETE FROM Quote WHERE QuoteId = {quote_id}')
        logger.info(f'Removed quote with ID {quote_id}')
    except KeyError as ex:
        logger.error('The specified key was not found', ex)


def by_list(list_file):
    f = open(list_file, 'r', encoding='utf-8-sig')
    for line in f:
        try:
            if not is_valid_quote_id(line):
                logger.warning(f'{line.strip()} was found as a list item but it is not a valid quote ID. Skipping...')
                continue

            quote_id = int(line)
            db.query(f'DELETE FROM Quote WHERE QuoteId = {quote_id}')
            logger.info(f'Removed {quote_id}')
        except KeyError as ex:
            logger.error(f'Key {ex} was not found ')
    f.close()


def duplicates():
    duplicates = []
    logger.info('Cleaning duplicates...')

    quotes = db.query('SELECT QuoteId, Text FROM Quote')

    for quote in quotes:
        truncated_quote = quote[1][:duplicate_threshold]

        sql = f"""
        WITH temp AS
        (
            SELECT row_number() over (order by QuoteId) RowNumber
            FROM Quote
            WHERE Text LIKE \"%{truncated_quote}%\"
        )
        SELECT *
        FROM temp
        WHERE RowNumber !=1
        """

        duplicate_quotes = db.query(sql)
    print(duplicate_quotes)

    logger.info(f'Removed {len(duplicates)} duplicate records')
