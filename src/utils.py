from settings import *
import json

def write_data_to_file(data, filepath):
    
    logging.info(f'Starting utils [write_data_to_file] ....... {filepath}')

    with open(filepath, 'w') as f:
        json.dump(data, f)
    
    logging.info(f'Finished utils [write_data_to_file] ....... {filepath}')

def read_data_from_file(filepath):
    
    logging.info(f'Starting utils [read_data_from_file] ....... {filepath}')

    with open(filepath, 'r') as f:
        data_dict = json.load(f)
    
    logging.info(f'Finished utils [read_data_from_file] ....... {filepath}')

    return data_dict

def create_connection():

    logging.info(f'Starting utils [create_connection] ....... {DB_PATH}')

    db_conn = None
    try:
        db_conn = sqlite3.connect(DB_PATH)
        return db_conn
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())

        logging.info(f'Script failed due to exception: utils [create_connection] ....... {DB_PATH}')

        if db_conn:
            db_conn.close()

def create_table(query, table_name):

    logging.info(f'Starting utils [create_table] ....... {table_name}')

    conn = create_connection()
    try:
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute(query)

            conn.commit()
            conn.close()
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())

        logging.info(f'Script failed due to exception: utils [create_table] ....... {table_name}')

        if conn:
            conn.close()


    logging.info(f'Finished utils [create_table] ....... {table_name}')

