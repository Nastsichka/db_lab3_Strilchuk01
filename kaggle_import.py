import psycopg2
import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np


username = 'postgres'
password = '11111111'
database = 'strilchuk_BD'
host = 'localhost'
port = '5432'


query_0 = """
DELETE FROM Poems;
DELETE FROM Authors;
DELETE FROM Periods;
DELETE FROM Genres;
"""

query_authors = """
INSERT INTO Authors(author_id, author_name) VALUES ('%s', '%s')
"""

query_periods = """
INSERT INTO Periods(period_id, period_name) VALUES ('%s', '%s')
"""

query_genres = """
INSERT INTO Genres(genre_id, genre_name) VALUES ('%s', '%s')
"""

query_poems = """
INSERT INTO Poems(poem_id, poem_name, poem_content, author_id, period_id, genre_id) 
VALUES ('%s', '%s', '%s', 
(SELECT author_id FROM authors WHERE author_name = '%s'), 
(SELECT period_id FROM periods WHERE period_name = '%s'),
(SELECT genre_id FROM genres WHERE genre_name = '%s'))
"""


data = pd.read_csv(r'kagglepoems.csv')

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()
    cur.execute(query_0)

    df = pd.DataFrame(data, columns=['poem name', 'content', 'author', 'age', 'type'])

    cur1 = conn.cursor()
    author_name = df['author'].tolist()

    unique_author_name = set(author_name)

    i = 0
    for el in unique_author_name:
        query = query_authors % (i, el)
        cur1.execute(query)
        i += 1
    conn.commit()


    cur2 = conn.cursor()
    period_name = df['age'].tolist()

    unique_period_name = set(period_name)

    i = 0
    for el in unique_period_name:
        query = query_periods % (i, el)
        cur2.execute(query)
        i += 1
    conn.commit()


    cur3 = conn.cursor()
    genre_name = df['type'].tolist()

    unique_genre_name = set(genre_name)

    i = 0
    for el in unique_genre_name:
        query = query_genres % (i, el)
        cur3.execute(query)
        i += 1
    conn.commit()


    cur4 = conn.cursor()
    poem_name = df['poem name'].tolist()
    poem_content = df['content'].tolist()

    unique_author_name = set(author_name)

    i = 0
    for i in range(len(poem_name)):
        if type(poem_name[i]) != float:
            poem_name[i] = poem_name[i].replace('\'', '')
        poem_content[i] = poem_content[i].replace('\'', '')
        query = query_poems % (i, poem_name[i], poem_content[i][0:9999], author_name[i], period_name[i], genre_name[i])
        cur4.execute(query)
    conn.commit()

