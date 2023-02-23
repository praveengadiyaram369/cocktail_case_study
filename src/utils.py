from settings import *
from db_utils import *
import json
import re
from fractions import Fraction

def write_data_to_file(data, filepath):
    
    with open(filepath, 'w') as f:
        json.dump(data, f)
    

def read_data_from_file(filepath):
    
    with open(filepath, 'r') as f:
        data_dict = json.load(f)
    
    return data_dict

def replace_word_to_float(measurement):
    
    for key, val in WORD_TO_FLOAT_DICT.items():
        if key in measurement:
            measurement = measurement.replace(key, val)
            break
    return measurement

def get_transform_fraction(measurement):
    
    fraction_regex = """\d \d\/\d|\d\/\d"""
    measurement = replace_word_to_float(measurement)
    
    fraction = re.findall(fraction_regex, measurement)
    if len(fraction) > 0:
        fraction = fraction[0]
        
        if len(fraction.split()) == 1:
            numeric_val = float(Fraction(fraction))
        elif len(fraction.split()) == 2:
            numeric_val = float(fraction.split()[0]) + float(Fraction(fraction.split()[1]))

        replace_str = str(round(numeric_val, 2))

        return re.sub(fraction_regex, replace_str, measurement)
    else:
        return measurement
    
def check_digit(text):
    
    return text.replace('.','',1).isdigit() or text.replace('-','',1).isdigit()
    
def get_transform_measurement_tokens(measurement):
    
    measurement = measurement.lower()
    measurement_tokens = measurement.split()
    
    quantity = None
    unit = None
    meta_data = None
    
    if len(measurement_tokens) == 2:
        if check_digit(measurement_tokens[0]) and check_digit(measurement_tokens[1]):
            quantity = measurement_tokens[0]+measurement_tokens[1]
            unit = 'NA'
            meta_data = 'NA'
        elif check_digit(measurement_tokens[0]) and not check_digit(measurement_tokens[1]):
            quantity = measurement_tokens[0]
            unit = measurement_tokens[1]
            meta_data = 'NA'
    elif len(measurement_tokens) == 1:
        if check_digit(measurement_tokens[0]):
            quantity = measurement_tokens[0]
            unit = 'NA'
            meta_data = 'NA'
        elif check_digit(measurement_tokens[0][0]):
            for idx in range(len(measurement_tokens[0])-1, -1, -1):
                if check_digit(measurement_tokens[0][idx]):
                     break
            
            quantity = measurement_tokens[0][:idx+1]
            unit = measurement_tokens[0][idx+1:]
            meta_data = 'NA'
        else:
            quantity = 'NA'
            unit = 'NA'
            meta_data = measurement_tokens[0]
    elif len(measurement_tokens) > 2:
        
        if check_digit(measurement_tokens[0]):
            quantity = measurement_tokens[0]
            unit = measurement_tokens[1]
            meta_data = ' '.join(measurement_tokens[2:])
            if unit in TARGET_UNITS:
                unit = 'NA'
                meta_data = ' '.join(measurement_tokens[1:])
        elif check_digit(measurement_tokens[-1]):
            quantity = measurement_tokens[-1]
            unit = 'NA'
            meta_data = ' '.join(measurement_tokens[:-1])
        else:
            
            for idx, token in enumerate(measurement_tokens):
                
                if check_digit(token):
                    quantity = token
                    unit = measurement_tokens[idx+1]
                    meta_data = ' '.join(measurement_tokens[:-idx-1])
                    break
            
        if quantity is None and unit is None and meta_data is None:
            quantity = 'NA'
            unit = 'NA'
            meta_data = measurement
            
    if quantity is None and unit is None and meta_data is None:
        quantity = 'NA'
        unit = 'NA'
        meta_data = 'NA'
        
    if unit in UNIT_MAPPING_DICT.keys():
        unit = UNIT_MAPPING_DICT[unit]
        
    if meta_data in UNIT_MAPPING_DICT.keys():
        meta_data = UNIT_MAPPING_DICT[meta_data]
        
    if meta_data in TARGET_META_DATA_FLIP:
        unit, meta_data = meta_data, unit
        
        if quantity is 'NA':
            quantity = str(1)
    elif unit in TARGET_UNIT_FLIP:
        unit, meta_data = meta_data, unit
        
    if '-' in quantity:
        min_quantity = float(quantity.split('-')[0])
        max_quantity = float(quantity.split('-')[1])
    elif quantity == 'NA':
        min_quantity = 0.0
        max_quantity = 0.0      
    else:
        min_quantity = 0.0
        max_quantity = float(quantity)

    return (min_quantity, max_quantity, unit, meta_data)

def get_dict_keys_data(data_dict, keys):

    return {k: v for k, v in data_dict.items() if k in keys}

def get_ingedients_data(data_dict):

    ingredients_dict = dict()
    for ingredient, measure in zip(INGREDIENTS_COLS, MEASURE_COLS):

        if data_dict[ingredient] is not None and data_dict[measure] is not None:
            measurement_fraction_transformed = get_transform_fraction(data_dict[measure].strip())
            measurement_tokens = get_transform_measurement_tokens(measurement_fraction_transformed)

            ingredients_dict[data_dict[ingredient].lower()] = measurement_tokens

    return ingredients_dict

def parse_data_from_file(filename):

    with open(filename, 'r') as f:
        data = f.read().splitlines()

    insert_data = []
    for val in data:
        insert_data.append(tuple(val.split(DELIMITER)))

    return insert_data

def insert_static_data_db(filename, table_name):

    filename = SQL_DATA_FILEPATH + filename + '.txt'

    data = parse_data_from_file(filename)
    insert_data_many(data, table_name)

def insert_dynamic_drinks_data():

    drinks_insert_data = []
    ingredients_insert_data = []

    for filename in os.listdir(DOWNLOAD_DATA_FILEPATH):
        if '.json' in filename:
            data = read_data_from_file(DOWNLOAD_DATA_FILEPATH+filename)
            drinks_list = data['drinks']

            if drinks_list is not None and len(drinks_list) > 0:

                for drink in drinks_list:
                    
                    if drink is not None:
                        drinks_data = get_dict_keys_data(drink, DRINKS_COLS)

                        if drinks_data['strInstructionsDE'] is not None:
                            drinks_insert_data.append(tuple(list(drinks_data.values())))

                            ingredients_dict = get_ingedients_data(drink)

                            for ingredient, measurement_tokens in ingredients_dict.items():
                                
                                drink_id = drinks_data['idDrink']
                                ingredients_id = get_reference_id('ingredients', col_name='ingredients_name', data=ingredient)
                                min_quantity = measurement_tokens[0]
                                max_quantity = measurement_tokens[1]
                                measurement_unit_id = get_reference_id('measurement_units', col_name='measurement_name', data=measurement_tokens[2])
                                meta_data = measurement_tokens[3]

                                ingredients_insert_data.append(tuple([drink_id, ingredients_id, min_quantity, max_quantity, measurement_unit_id, meta_data]))

    insert_data_many(drinks_insert_data, 'cocktail_drinks')
    insert_data_many(ingredients_insert_data, 'cocktail_ingredients')