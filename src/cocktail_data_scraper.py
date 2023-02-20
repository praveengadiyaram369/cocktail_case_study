import requests
import sys
from settings import *
from utils import *

def get_url_api_response(input_url, filename):

    logging.info(f'Starting cocktail_data_scraper [get_url_api_response] ....... {filename}')

    api_response_json = requests.get(input_url).json()
    #response_dict = json.loads(api_response_json)

    write_data_to_file(api_response_json, DOWNLOAD_DATA_FILEPATH+filename+'.json')

    logging.info(f'Finished cocktail_data_scraper [get_url_api_response] ....... {filename}')

def download_data():

    logging.info('Starting cocktail_data_scraper [download_data] ....... ')

    try:
        for cocktail_first_letter in ALPHABET_LIST:
            cocktail_first_letter_url = f'https://www.thecocktaildb.com/api/json/v1/1/search.php?f={cocktail_first_letter}'
            print(cocktail_first_letter_url)

            get_url_api_response(cocktail_first_letter_url, cocktail_first_letter)

    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())

        logging.info('Script failed due to exception: cocktail_data_scraper [download_data] ....... ')
    
    logging.info('Finished cocktail_data_scraper [download_data] ....... ')

def create_db_tables():
    
    logging.info('Starting cocktail_data_scraper [create_db_tables] ....... ')

    try:
        create_table(CREATE_TABLE_COCKTAIL_DRINKS, 'cocktail_drinks')
        create_table(CREATE_TABLE_INGREDIENTS, 'ingredients')
        create_table(CREATE_TABLE_COCKTAIL_INGREDIENTS, 'cocktail_ingredients')

    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())

        logging.info('Script failed due to exception: cocktail_data_scraper [create_db_tables] ....... ')
    
    logging.info('Finished cocktail_data_scraper [create_db_tables] ....... ')

def insert_data_to_db():
    
    logging.info('Starting cocktail_data_scraper [insert_data_to_db] ....... ')

    try:
        create_tables()

    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())

        logging.info('Script failed due to exception: cocktail_data_scraper [insert_data_to_db] ....... ')
    
    logging.info('Finished cocktail_data_scraper [insert_data_to_db] ....... ')


if __name__ == '__main__':

    logging.info('Starting cocktail_data_scraper [main] ....... ')

    input_args = sys.argv
    if input_args[1] == 'DOWNLOAD_DATA':
        download_data()
    elif input_args[1] == 'CREATE_TABLES':
        create_db_tables()
    elif input_args[1] == 'INSERT_DATA':
        insert_data_to_db()

    logging.info('Finished cocktail_data_scraper [main] ....... ')
