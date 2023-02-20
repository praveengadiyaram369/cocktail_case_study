import string
import os
import logging
import traceback
import sqlite3

ALPHABET_LIST = string.ascii_lowercase
DOWNLOAD_DATA_FILEPATH = os.getcwd() + '/data/'

LOG_FILENAME = os.getcwd() + '/logs/cocktail_data_logger.log'
logging.basicConfig(handlers=[logging.FileHandler(filename=LOG_FILENAME, 
                    encoding='utf-8', mode='a+')],
                    level=logging.INFO)

DB_PATH = os.getcwd() + '/sqlite_db/sqlite_cocktail_db.db'

CREATE_TABLE_COCKTAIL_DRINKS = """CREATE TABLE IF NOT EXISTS cocktail_drinks (
                                id INTEGER PRIMARY KEY,
                                drink_name TEXT NOT NULL,
                                drink_alternate TEXT ,
                                tags TEXT ,
                                Video TEXT ,
                                Category TEXT ,
                                IBA TEXT ,
                                alcoholic TEXT ,
                                glass TEXT ,
                                instructions TEXT ,
                                drinkthumb TEXT ,
                                imagesource TEXT ,
                                imageattribution TEXT ,
                                creativecommonsconfirmed TEXT ,
                                datemodified timestamp 
                                );"""

CREATE_TABLE_INGREDIENTS = """CREATE TABLE IF NOT EXISTS ingredients (
                                id INTEGER PRIMARY KEY,
                                ingredients_name TEXT NOT NULL,
                                ingredients_unit TEXT NOT NULL
                                );"""

CREATE_TABLE_COCKTAIL_INGREDIENTS = """CREATE TABLE IF NOT EXISTS cocktail_ingredients (
                                drink_id TEXT NOT NULL,
                                ingredients_id TEXT NOT NULL,
                                measure TEXT NOT NULL,
                                PRIMARY KEY (drink_id, ingredients_id)
                                FOREIGN KEY (drink_id) REFERENCES cocktail_drinks (id),
                                FOREIGN KEY (ingredients_id) REFERENCES ingredients (id)
                                );"""