import re
import logging
import sys

logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))

def parse_author(data):
    regex = re.compile(r'(?<=\().*(?=\))')
    try:
        author = regex.search(data)
        return author.group(0)
    except AttributeError:
        logger.error('Unable to parse author. Setting as empty...')
        return ''

def parse_text(sentence):
    words = sentence.split(" ")
    return [word for word in words if word.isalnum()]

class Quote:
    def __init__(self, data):
        book = data[0][:data[0].find('(')]
        self.__author = parse_author(data[0])
        self.__book = book
        self.__metadata = Metadata(data[2])
        self.__text = parse_text(data[3])

    @property
    def author(self):
        return self.__author

    @property
    def book(self):
        return self.__book

    @property
    def text(self):
        return self.__text


class Metadata:
    def __init__(self, data):
        self._page = data[0]
        self._location = data[0]
        self._timestamp = data[0]
