import string
import os
import logging
import traceback
import sqlite3

DELIMITER = '||'
ALPHABET_LIST = string.ascii_lowercase
DOWNLOAD_DATA_FILEPATH = os.getcwd() + '/data/'
SQL_DATA_FILEPATH = os.getcwd() + '/sql_data/'

DB_PATH = os.getcwd() + '/sqlite_db/sqlite_cocktail_db.db'

LOG_FILENAME = os.getcwd() + '/logs/cocktail_data_logger.log'
logging.basicConfig(handlers=[logging.FileHandler(filename=LOG_FILENAME, 
                    encoding='utf-8', mode='a+')],
                    level=logging.INFO)


CREATE_TABLE_COCKTAIL_DRINKS = """CREATE TABLE IF NOT EXISTS cocktail_drinks (
                                id INTEGER PRIMARY KEY,
                                drink_name TEXT NOT NULL,
                                drink_alternate TEXT ,
                                tags TEXT ,
                                video TEXT ,
                                category TEXT ,
                                iba TEXT ,
                                alcoholic TEXT ,
                                glass TEXT ,
                                instructions TEXT ,
                                instructionsde TEXT ,
                                drinkthumb TEXT ,
                                imagesource TEXT ,
                                imageattribution TEXT ,
                                creativecommonsconfirmed TEXT ,
                                datemodified timestamp 
                                );"""

CREATE_TABLE_INGREDIENTS = """CREATE TABLE IF NOT EXISTS ingredients (
                                id INTEGER PRIMARY KEY,
                                ingredients_name TEXT NOT NULL
                                );"""

CREATE_TABLE_MEASUREMENT_UNITS = """CREATE TABLE IF NOT EXISTS measurement_units (
                                id INTEGER PRIMARY KEY,
                                measurement_name TEXT NOT NULL
                                );"""

CREATE_TABLE_COCKTAIL_INGREDIENTS = """CREATE TABLE IF NOT EXISTS cocktail_ingredients (
                                drink_id INTEGER NOT NULL,
                                ingredients_id INTEGER NOT NULL,
                                min_quantity REAL NOT NULL,
                                max_quantity REAL NOT NULL,
                                measurement_unit_id INTEGER NOT NULL,
                                meta_data TEXT,
                                PRIMARY KEY (drink_id, ingredients_id),
                                FOREIGN KEY (drink_id) REFERENCES cocktail_drinks (id),
                                FOREIGN KEY (ingredients_id) REFERENCES ingredients (id),
                                FOREIGN KEY (measurement_unit_id) REFERENCES measurement_units (id)
                                );"""

CREATE_TABLE_MEASUREMENT_UNIT_CONVERSION = """CREATE TABLE IF NOT EXISTS measurement_conversion (
                                id INTEGER PRIMARY KEY,
                                measurement_from_id TEXT NOT NULL,
                                measurement_to_id TEXT NOT NULL,
                                conversion_multiplying_factor REAL NOT NULL,
                                FOREIGN KEY (measurement_from_id) REFERENCES measurement_units (id),
                                FOREIGN KEY (measurement_to_id) REFERENCES measurement_units (id)
                                );"""

WORD_TO_FLOAT_DICT = {' third': '/3',
                      ' fourth': '/4',
                      ' fifth': '/5',
                      ' sixth': '/6',
                      ' seventh': '/7',
                      ' eigth': '/8',
                      ' nineth': '/9',
                      ' tenth': '/10',
                      '½': '1/2'
                     }

TARGET_UNITS = ['or', 'smirnoff']

TARGET_META_DATA_FLIP = ['pinch', 'bottle', 'cube', 'dash', 'splash', 'sprig', 'wedge', 'strip', 'measure', 'leaf']
TARGET_UNIT_FLIP = ['fresh']

UNIT_MAPPING_DICT = {
                    'bottles': 'bottle',
                    'cans': 'can',
                    'chunks': 'chunk',
                    'cubes': 'cube',
                    'cups': 'cup',
                    'dashes': 'dash',
                    'drops': 'drop',
                    'glasses': 'glass',
                    'inches': 'inch',
                    'jiggers': 'jigger',
                    'measures': 'measure',
                    'packages': 'package',
                    'parts': 'part',
                    'pieces': 'piece',
                    'pinches': 'pinch',
                    'pints': 'pint',
                    'shots': 'shot',
                    'slices': 'slice',
                    'splashes': 'splash',
                    'sprigs': 'sprig',
                    'sticks': 'stick',
                    'wedges': 'wedge',
                    'tblsp': 'tbsp',
                    'scoops': 'scoop',
                    'strips': 'strip',
                    'leaves': 'leaf'
                    }

DRINKS_COLS = ['idDrink',
                'strDrink',
                'strDrinkAlternate',
                'strTags',
                'strVideo',
                'strCategory',
                'strIBA',
                'strAlcoholic',
                'strGlass',
                'strInstructions',
                'strInstructionsDE',
                'strDrinkThumb',
                'strImageSource',
                'strImageAttribution',
                'strCreativeCommonsConfirmed',
                'dateModified'
                ]

INGREDIENTS_COLS = ['strIngredient1',
                    'strIngredient2',
                    'strIngredient3',
                    'strIngredient4',
                    'strIngredient5',
                    'strIngredient6',
                    'strIngredient7',
                    'strIngredient8',
                    'strIngredient9',
                    'strIngredient10',
                    'strIngredient11',
                    'strIngredient12',
                    'strIngredient13',
                    'strIngredient14',
                    'strIngredient15'
                    ]

MEASURE_COLS = ['strMeasure1',
                'strMeasure2',
                'strMeasure3',
                'strMeasure4',
                'strMeasure5',
                'strMeasure6',
                'strMeasure7',
                'strMeasure8',
                'strMeasure9',
                'strMeasure10',
                'strMeasure11',
                'strMeasure12',
                'strMeasure13',
                'strMeasure14',
                'strMeasure15'
                ]
