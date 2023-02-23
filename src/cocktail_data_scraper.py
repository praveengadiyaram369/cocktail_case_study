import requests
import sys
from settings import *
from utils import *


def get_url_api_response(input_url, filename):
    """This method get_url_api_response scrapes cocktail drinks data using api interface.
    The response of the api is stored as a json file.

    Downloading the data to a json file helps not to hit the api multiple times.
    """
    logging.info(
        f"Starting cocktail_data_scraper [get_url_api_response] ....... {filename}"
    )

    api_response_json = requests.get(input_url).json()
    write_data_to_file(api_response_json, DOWNLOAD_DATA_FILEPATH + filename + ".json")

    logging.info(
        f"Finished cocktail_data_scraper [get_url_api_response] ....... {filename}"
    )


def download_data():
    """This method download_data creates a specific api request to download the cocktail drinks that start
    with a particular character. In this way, all the drinks can be accessed with just changing the first letter
    in the api request.
    """
    logging.info("Starting cocktail_data_scraper [download_data] ....... ")

    try:
        for cocktail_first_letter in ALPHABET_LIST:
            cocktail_first_letter_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={cocktail_first_letter}"

            get_url_api_response(cocktail_first_letter_url, cocktail_first_letter)

    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())

        logging.info(
            "Script failed due to exception: cocktail_data_scraper [download_data] ....... "
        )

    logging.info("Finished cocktail_data_scraper [download_data] ....... ")


def create_db_tables():
    """This method create_db_tables creates schema by creating all the tables in the db.
    Actual queries used for the table creation can be found in settings.py
    """
    logging.info("Starting cocktail_data_scraper [create_db_tables] ....... ")

    try:
        create_table(CREATE_TABLE_COCKTAIL_DRINKS, "cocktail_drinks")
        create_table(CREATE_TABLE_INGREDIENTS, "ingredients")
        create_table(CREATE_TABLE_MEASUREMENT_UNITS, "measurement_units")
        create_table(CREATE_TABLE_COCKTAIL_INGREDIENTS, "cocktail_ingredients")
        create_table(CREATE_TABLE_MEASUREMENT_UNIT_CONVERSION, "measurement_conversion")

    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())

        logging.info(
            "Script failed due to exception: cocktail_data_scraper [create_db_tables] ....... "
        )

    logging.info("Finished cocktail_data_scraper [create_db_tables] ....... ")


def insert_data_to_db():
    """The insert_data_to_db inserts data into all tables according to the db schema created before.

    1. Primarily data is split into static and dynamic data.
    2. Static data deals with ingredient names, measurement units, rules for the conversions usw.
       This data is common for many drinks and re-used many times.

    3. Dynamic data is the data specifically related to the drinks and dependent on scraped results.
    """
    logging.info("Starting cocktail_data_scraper [insert_data_to_db] ....... ")

    try:
        insert_static_data_db(filename="ingredients", table_name="ingredients")
        insert_static_data_db(
            filename="measurement_units", table_name="measurement_units"
        )
        insert_static_data_db(
            filename="measurement_conversions", table_name="measurement_conversion"
        )

        insert_dynamic_drinks_data()

    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())

        logging.info(
            "Script failed due to exception: cocktail_data_scraper [insert_data_to_db] ....... "
        )

    logging.info("Finished cocktail_data_scraper [insert_data_to_db] ....... ")


if __name__ == "__main__":
    """The main function handles all methods to scrape data, create tables and insert
     data into the tables and is operated by using the commandline arguments.

    Usage instructions: all execute the commands from the project folder

     1. To download the api data:
        python src/cocktail_data_scraper.py DOWNLOAD_DATA

     2. To create tables in the database
        python src/cocktail_data_scraper.py CREATE_TABLES

     3. To insert data inside the tables
        python src/cocktail_data_scraper.py INSERT_DATA

     4. To perform all operations sequentially
        python src/cocktail_data_scraper.py

    """
    logging.info("Starting cocktail_data_scraper [main] ....... ")

    input_args = sys.argv
    if len(input_args) > 1:
        if input_args[1] == "DOWNLOAD_DATA":
            download_data()
        elif input_args[1] == "CREATE_TABLES":
            create_db_tables()
        elif input_args[1] == "INSERT_DATA":
            insert_data_to_db()
    else:
        download_data()
        create_db_tables()
        insert_data_to_db()


    logging.info("Finished cocktail_data_scraper [main] ....... ")