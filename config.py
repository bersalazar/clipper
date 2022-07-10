import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "db_host": os.environ["DBHOST"],
    "db_user": os.environ["DBUSER"],
    "db_name": os.environ["DBNAME"],
    "db_port": os.environ["DBPORT"],
    "db_password": os.environ["DBPASSWORD"],
    "duplicate_search_substring_threshold": 25,
    "pdf_output_path": "quotes.pdf",
    "starred_pdf_output_path": "starred-quotes.pdf",
    "default_deletable_quotes_file": "files/deletable_quotes",
}
