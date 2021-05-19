import re
import mariadb

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
    def __init__(self, block):
        book = block[0][:block[0].find('(')].strip()
        self.__book = book
        self.__author = parse_author(block[0])
        self.__metadata = Metadata(block[2])
        self.__text = block[3]
        self.__date = parse_date(block[1])
        self.__page = parse_page(block[1])
        self.__location = parse_location(block[1])
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
    def date(self):
        return self.__date

    @property
    def page(self):
        return self.__page

    @property
    def location(self):
        return self.__location

    #def is_found(self, db):
    #    return db.search(Query().text.matches(self.text))


class Metadata:
    def __init__(self, data):
        self._page = data[0]
        self._location = data[0]
        self._timestamp = data[0]


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

    def __is_committable_query(self, sql):
        if sql.startswith('INSERT') or sql.startswith('DELETE') or sql.startswith('UPDATE'):
            return True
        return False

    def query(self, sql):
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            logger.debug(sql)
            if self.__is_committable_query(sql):
                self.conn.commit()

            try:
                return cursor.fetchall()
            except mariadb.ProgrammingError as ex:
                if ex.errmsg == "Cursor doesn't have a result set":
                    return
                raise ex
