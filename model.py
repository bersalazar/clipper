import re
import sys
import logging
from tinydb import Query

logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))


def parse_author(data):
    regex = re.compile(r'(?<=\().*(?=\))')
    try:
        author = regex.search(data)
        return author.group(0)
    except AttributeError:
        logger.warning('Unable to parse author. Setting as empty...')
        return ''


class Quote:
    def __init__(self, block):
        book = block[0][:block[0].find('(')]
        self.__book = book
        self.__author = parse_author(block[0])
        self.__metadata = Metadata(block[2])
        self.__text = block[3]
        self.__block = block


    @property
    def author(self):
        return self.__author

    @property
    def book(self):
        return self.__book

    @property
    def text(self):
        return self.__text
     
    @property
    def block(self):
        return self.__block

    def is_found(self, db):
        return db.search(Query().text.matches(self.text))


class Metadata:
    def __init__(self, data):
        self._page = data[0]
        self._location = data[0]
        self._timestamp = data[0]
