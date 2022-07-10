import re
import mariadb
import json

from logger import logger
from datetime import datetime


def parse_author(data):
    regex = re.compile(r'(?<=\().*(?=\))')
    try:
        author = regex.search(data)
        return author.group(0)
    except AttributeError:
        #logger.debug(f'Unable to parse author from {data}')
        return ''


def parse_location(data):
    regex = re.compile(r'Location [0-9]+-[0-9]+|Location [0-9]+')
    try:
        result = regex.search(data).group(0)
        location = result[result.find(" "):].strip()
        return location
    except AttributeError:
        #logger.debug(f'Unable to parse location from {data}')
        return ''


def parse_date(data):
    regex = re.compile(r'[A-Za-z]+, [A-Za-z]+ [0-9]+, [0-9]+')
    try:
        date = regex.search(data)
        return datetime.strptime(date.group(0), '%A, %B %d, %Y').date()
    except AttributeError:
        #logger.debug(f'Unable to parse date from {data}')
        return ''


def parse_page(data):
    regex = re.compile(r'page [0-9]+')
    try:
        result = regex.search(data).group(0)
        page = result[result.find(" "):].strip()
        return page
    except AttributeError:
        #logger.debug(f'Unable to parse page from {data}')
        return 0


class Quote:
    def __init__(self, text, date, page, location, book_id="", author_id="", author="", book=""):
        self.__text = text
        self.__date = date
        self.__page = page
        self.__location = location
        self.__book_id = book_id
        self.__author_id = author_id
        self.__author = author
        self.__book = book

    @classmethod
    def from_block(cls, block):
        book = block[0][:block[0].find('(')].strip()
        return cls(
            text=block[3],
            date=parse_date(block[1]),
            page=parse_page(block[1]),
            location=parse_location(block[1]),
            author=parse_author(block[0]),
            book=book
        )

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
    def date(self):
        return self.__date

    @property
    def page(self):
        return self.__page

    @property
    def location(self):
        return self.__location

    @property
    def book_id(self):
        return self.__book_id

    @property
    def author_id(self):
        return self.__author_id

    def __repr__(self):
        return f'Quote({self.text}, {self.date}, {self.page}, {self.location}, {self.author_id}, {self.book_id})'

    def as_json(self):
        return json.dumps({
            "text": self.__text,
            "date": self.__date.strftime("%Y%m%d"),
            "page": self.__page,
            "location": self.__location,
            "book_id": self.__book_id,
            "author_id": self.__author_id,
            "author": self.__author,
            "book": self.__book
        })


class Db:
    def __init__(self, host, database, port, user, password):
        port = int(port) if type(port) is not int else port
        self.conn = mariadb.connect(
            host=host,
            database=database,
            port=port,
            user=user,
            password=password
        )

    def __del__(self):
        self.conn.close()

    def _is_committable_query(self, sql):
        if 'INSERT' in sql or 'DELETE' in sql or 'UPDATE' in sql:
            return True
        return False

    def query(self, sql):
        with self.conn.cursor() as cursor:
            logger.debug(sql)
            cursor.execute(sql)
            if self._is_committable_query(sql):
                self.conn.commit()

            try:
                return cursor.fetchall()
            except mariadb.ProgrammingError as ex:
                if ex.errmsg == "Cursor doesn't have a result set":
                    return
                raise ex
