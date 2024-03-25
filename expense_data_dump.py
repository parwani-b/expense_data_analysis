import os
import sys
import yaml
import time
import logging
import pandas as pd
from datetime import datetime
import numpy as np
from sqlalchemy import create_engine
import pymysql
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

# Data Warehouse Connection
def dw_connect():
    dw_connection_info = config['db_connection_info']['expense_data_warehouse']
    dw_connection = pymysql.connect(**dw_connection_info)
    dw_cursor = dw_connection.cursor()
    dw_engine = create_engine(
        'mysql+pymysql://' + dw_connection_info['user'] + ':' + dw_connection_info['passwd'] + '@' + dw_connection_info[
            'host'] + ':' + str(3306) + '/' + dw_connection_info['db'], echo=False)
    return dw_connection, dw_cursor, dw_engine
    
# Exception handling logging
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    
# Get the start datetime when the program runs
run_start_date = datetime.now().replace(microsecond=0)

# Load config
config = yaml.load(open('config.yml'), Loader=yaml.FullLoader)

# Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)
handler = logging.FileHandler(config['paths']['log_path'])
handler.setFormatter(formatter)
logger.addHandler(handler)
sys.excepthook = handle_exception

dw_connection, dw_cursor, dw_engine = dw_connect()

# Previous run data
# dw_cursor.execute("select max(date) from personal_2023_04_01_export")
dw_cursor.execute("select max(date) from personal_2024_export")
most_recent_expense_date = dw_cursor.fetchone()
if most_recent_expense_date[0] is None: 
    most_recent_expense_date = datetime.strptime("1/2/2017", "%m/%d/%Y").date()
else:
    most_recent_expense_date = most_recent_expense_date[0]
    
# Delete the most recent date loaded (in case any program crashed last time)

# dw_cursor.execute("delete from personal_2023_04_01_export where date >= %s", most_recent_expense_date)
# dw_cursor.execute("delete from personal_2024_export where date >= %s", most_recent_expense_date)
# dw_connection.commit()

# TODO: Delete the empty rows from spreadsheet and change the file name every time you download a new spreadsheet and run this script
splitwiseData = pd.read_csv("C:\\Users\\Bharat Parwani\\Bharat_Data\\expense_data\\personal_2024-03-24_export.csv", index_col=False, parse_dates=['Date'])
print(splitwiseData.dtypes)

# Dropping columns 'Bharat' and 'Currency' from the dataframe
splitwiseData = splitwiseData.drop(['Bharat', 'Currency'], axis=1)
# splitwiseData.head()

splitwiseData.insert(0, 'Id', range(1, 1 + len(splitwiseData)))
splitwiseData.set_index('Id', append=True).reset_index(level=0)

# Converting 'Date' column to datetime data format
splitwiseData['Date'] = pd.to_datetime(splitwiseData['Date'], errors='coerce')

# I found that the splitwise export data also has a row at the end that says "Total balance" but the cost value for that 
# is null value which causes problem in insertion of data in MySQL

# Truncates the existing data in MySQL table
print("\nTruncating all the previous expense data...\n")
truncate_query = "TRUNCATE TABLE personal_2024_export"
dw_cursor.execute(truncate_query)
print("Success! All the previous data in the back-end table has now been truncated!\n")

# splitwiseData.to_sql(con=dw_engine, name='personal_2023_04_01_export', if_exists='append', chunksize=1, index=False)
print("Storing new data in progress...\n")
splitwiseData.to_sql(con=dw_engine, name='personal_2024_export', if_exists='append', chunksize=1, index=False)

print("\nSuccess! Latest expense data has been stored in the MySQL data warehouse!")