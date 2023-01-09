import csv
import psycopg2

username = 'postgres'
password = '11111111'
database = 'strilchuk_BD'
host = 'localhost'
port = '5432'

OUTPUT_FILE_T = 'poems_{}.csv'

TABLES = [
    'authors',
    'genres',
    'periods',
    'poems'
]

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()

    for tablename in TABLES:
        cur.execute('SELECT * FROM ' + tablename)
        fields = [x[0] for x in cur.description]
        with open(OUTPUT_FILE_T.format(tablename), 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(fields)
            for row in cur:
                writer.writerow([str(x) for x in row])
