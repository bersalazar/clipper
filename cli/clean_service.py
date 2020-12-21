from logger import logger
from tinydb import TinyDB
from config import config

db_path = config['database_path']
db = TinyDB(db_path)


def clean_by_key(args):
    try:
        db.remove(doc_ids=[int(args.key)])
        logger.info(f'Removed quote with ID {args.key}')
    except KeyError as ex:
        logger.error('The specified key was not found', ex)


def clean_by_list(args):
    f = open(args.list, 'r', encoding='utf-8-sig')
    for line in f:
        try:
            key = int(line)
            db.remove(doc_ids=[key])
            logger.info(f'Removed {key}')
        except KeyError as ex:
            logger.error(f'Key {ex} was not found ')
    f.close()


def clean_duplicates():
    previous_quote = ''
    duplicates = []
    logger.info('Cleaning duplicates...')
    for quote in db:
        if quote['text'].startswith(previous_quote[:25]):
            duplicates.append(quote.doc_id-1)
        previous_quote = quote['text']
    duplicates.pop(0)
    db.remove(doc_ids=duplicates)
    logger.info(f'Removed {len(duplicates)} duplicate records')
