#!/usr/local/bin/python3

import mariadb
import sys
from config import config

try:
    conn = mariadb.connect(
        host=config['db_host'],
        database=config['db_name'],
        port=int(config['db_port']),
        user=config['db_user'],
        password=config['db_password']
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB {e}")
    sys.exit(1)

cur = conn.cursor()

queries = [
    "DROP DATABASE kindle",
    "CREATE OR REPLACE DATABASE kindle",

    # Tables
    """
    CREATE TABLE kindle.Book (
        BookId int NOT NULL AUTO_INCREMENT,
        Name varchar(255),
        AuthorId int,
        PRIMARY KEY(BookId)
    )
    """,
    """
    CREATE TABLE kindle.Author (
        AuthorId int NOT NULL AUTO_INCREMENT,
        Name varchar(255),
        PRIMARY KEY(AuthorId))
    """,
    """
    CREATE TABLE kindle.Quote (
        QuoteId int NOT NULL AUTO_INCREMENT,
        Text varchar(2000),
        DateAdded date,
        Page int,
        Location varchar(255),
        BookId int,
        AuthorId int,
        PRIMARY KEY (QuoteId))
    """,
    """
    CREATE TABLE kindle.Temporary (
        QuoteId int NOT NULL AUTO_INCREMENT,
        Text varchar(2000),
        DateAdded date,
        Page int,
        Location varchar(255),
        BookId int,
        AuthorId int,
        PRIMARY KEY (QuoteId))
    """,

    # Foreign keys
    "ALTER TABLE kindle.Book ADD CONSTRAINT Author_FK FOREIGN KEY (AuthorId) REFERENCES kindle.Author(AuthorId)",
    "ALTER TABLE kindle.Quote ADD CONSTRAINT Quote_Book_FK FOREIGN KEY (BookId) REFERENCES kindle.Book(BookId)",
    "ALTER TABLE kindle.Quote ADD CONSTRAINT Quote_Author_FK FOREIGN KEY (AuthorId) REFERENCES kindle.Author(AuthorId)",
    "ALTER TABLE kindle.Temporary ADD CONSTRAINT Temporary_Book_FK FOREIGN KEY (BookId) REFERENCES kindle.Book(BookId)",
    "ALTER TABLE kindle.Temporary ADD CONSTRAINT Temporary_Author_FK FOREIGN KEY (AuthorId) REFERENCES kindle.Author(AuthorId)"
]

for query in queries:
    cur.execute(query)

authors = [
    (1, "Guy Patterson")
]
cur.executemany("INSERT INTO kindle.Author VALUES (?, ?)", authors)

books = [
    (1, "The Wonders", 1)
]
cur.executemany("INSERT INTO kindle.Book VALUES (?, ?, ?)", books)

cur.execute("insert into kindle.Temporary values (1, 'I am Spartacus', '2021-05-03', 5, 'Loc 2-3', 1, 1)")
cur.execute("insert into kindle.Quote values (1, 'I am Spartacus', '2021-05-03', 5, 'Loc 2-3', 1, 1)")

conn.commit()

cur.execute(
    """
    SELECT q.QuoteId, a.Name, b.Name FROM kindle.Quote q, kindle.Author a, kindle.Book b WHERE q.BookId = b.BookId and b.AuthorId = a.AuthorId
    """
)

print([row for row in cur])
