import pandas as pd
import sqlite3

def read_table(cursor, table, columns):
    '''
    reads the table data into a dataframe
    parameters: cursor, a connection cursor object
    table, a string of the table name
    columns, a list of strings which are the names of the columns of the new dataframe
    return: df, a dataframe with the table data
    '''
    cursor.execute(f'''SELECT * FROM {table}''')
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=columns)
    df = df.set_index('id')
    return df

def fetch_text_labels(dataset_path):
    '''
    extracts the labels and text tables from the database and load it into a
    dataframe
    parameters: dataset_path, string, contains the path to the .db file
    return: text, dataframe contains the id as the index and text column with the tweets
    labels, dataframe contains the id as the index and label column indicating the tweet class
    '''
    conn = sqlite3.connect(dataset_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    text = read_table(cursor, tables[0][0], columns=['id', 'text'])
    labels = read_table(cursor, tables[1][0], columns=['id', 'label'])
    return text, labels