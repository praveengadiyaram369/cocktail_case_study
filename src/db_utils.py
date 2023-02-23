from settings import *

def create_connection():

    logging.info(f'Starting db_utils [create_connection] ....... {DB_PATH}')

    db_conn = None
    try:
        db_conn = sqlite3.connect(DB_PATH)
        return db_conn
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())

        logging.info(f'Script failed due to exception: db_utils [create_connection] ....... {DB_PATH}')

        if db_conn:
            db_conn.close()

def create_table(query, table_name):

    logging.info(f'Starting db_utils [create_table] ....... {table_name}')

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

        logging.info(f'Script failed due to exception: db_utils [create_table] ....... {table_name}')

        if conn:
            conn.close()

    logging.info(f'Finished db_utils [create_table] ....... {table_name}')

def insert_data_many(data, table_name):

    logging.info(f'Starting db_utils [insert_data_many] ....... {table_name}')

    col_len = len(data[0])
    placeholder_str = ''.join(['?,' for val in range(col_len)])[:-1]

    insert_query = f'INSERT INTO {table_name} VALUES({placeholder_str})'

    conn = create_connection()
    try:
        if conn is not None:
            cursor = conn.cursor()
            cursor.executemany(insert_query, data)

            conn.commit()
            conn.close()
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())

        logging.info(f'Script failed due to exception: db_utils [insert_data_many] ....... {table_name}')

        if conn:
            conn.close()

    logging.info(f'Finished db_utils [insert_data_many] ....... {table_name}')

def get_reference_id(table_name, col_name, data):

    logging.info(f'Starting db_utils [get_reference_id] ....... {table_name}')

    select_query = f'SELECT id FROM {table_name} WHERE {col_name} = ?'

    conn = create_connection()
    try:
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute(select_query, (data,))

            row = cursor.fetchone()
            reference_id = row[0]

            conn.close()

            return reference_id
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())

        logging.info(f'Script failed due to exception: db_utils [get_reference_id] ....... {table_name}')

        if conn:
            conn.close()

    logging.info(f'Finished db_utils [get_reference_id] ....... {table_name}')

    