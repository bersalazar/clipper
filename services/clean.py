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


def search_quote_duplicates(quote):
    '''
    Searches and returns all the duplicates for a single quote.
    '''
    search_substring = quote[1][:config['duplicate_search_substring_threshold']]
    sql = f"""
    WITH temp AS
    (
        SELECT QuoteId, Text, row_number() over (order by QuoteId) RowNumber
        FROM Quote
        WHERE Text LIKE \"%{search_substring}%\"
    )
    SELECT *
    FROM temp
    WHERE RowNumber < (SELECT max(RowNumber) FROM temp)
    """

    return db.query(sql)


def duplicates():
    '''
    Cleans the database from duplicates. Grabs each quote and searches other occurences based on a threshold value.
    '''
    logger.info('Cleaning duplicates...')

    all_duplicates = []
    for quote in get_all_quotes():
        quote_duplicates = search_quote_duplicates(quote)
        if quote_duplicates:
            for duplicate in quote_duplicates:
                all_duplicates.append(duplicate[0])

    # When a list is passed to set(), only uniques are grabbed
    unique_duplicates = set(all_duplicates)
    amount_of_duplicates = len(unique_duplicates)
    if amount_of_duplicates > 0:
        print(f"All duplicate IDs: {unique_duplicates}")

        if input("Would you like to remove them? [y/N]: ") == "y":
            for quote_id in unique_duplicates:
                sql = f"DELETE FROM Quote WHERE QuoteId = {quote_id}"
                db.query(sql)
        else:
            exit(0)

    logger.info(f'Removed {amount_of_duplicates} duplicate records')
