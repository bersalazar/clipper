from logger import logger
from tinydb import TinyDB
from config import config

db_path = config['database_path']

duplicate_threshold = 25


def by_key(args):
    try:
        TinyDB(db_path).remove(doc_ids=[int(args.key)])
        logger.info(f'Removed quote with ID {args.key}')
    except KeyError as ex:
        logger.error('The specified key was not found', ex)


def by_list(list_file):
    f = open(list_file, 'r', encoding='utf-8-sig')
    for line in f:
        try:
            key = int(line)
            TinyDB(db_path).remove(doc_ids=[key])
            logger.info(f'Removed {key}')
        except KeyError as ex:
            logger.error(f'Key {ex} was not found ')
    f.close()


def duplicates():
    db = TinyDB(db_path)
    previous_quote = ''
    duplicates = []
    logger.info('Cleaning duplicates...')
    for quote in db:
        if quote['text'].startswith(previous_quote[:duplicate_threshold]):
            duplicates.append(quote.doc_id-1)
        previous_quote = quote['text']
    duplicates.pop(0)
    db.remove(doc_ids=duplicates)
    logger.info(f'Removed {len(duplicates)} duplicate records')
    db.close()
