import psycopg2
import pandas as pd

conn = psycopg2.connect(host='',
                        port='', 
                        dbname='',  
                        user='', 
                        password='')

conn.set_session(readonly=True)

cur = conn.cursor()

cur.execute("SELECT * FROM table_name")

data = cur.fetchall()

columns = [desc[0] for desc in cur.description]

df = pd.DataFrame(data, columns=columns)

cur.close()
conn.close()

if __name__ == '__main__':
    print(df.info(), end='\n\n\n')
    print(df.head())