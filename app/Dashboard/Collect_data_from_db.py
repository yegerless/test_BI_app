import psycopg2
from sshtunnel import SSHTunnelForwarder
import pandas as pd


server = SSHTunnelForwarder(('185.91.53.192', 5000), 
                            ssh_username='root',
                            ssh_password='BoNGbIakv8y0', 
                            remote_bind_address=('127.0.0.1', 5432),
                            # local_bind_address=('127.0.0.1', 5432)
                            )
server.start()



conn = psycopg2.connect(dbname='regions_django',  
                        user='regions_django', 
                        host=server.local_bind_host,
                        port=server.local_bind_port,
                        password='YjdsqGfhjkmairlow74')

conn.set_session(readonly=True)

cur = conn.cursor()

cur.execute("SELECT * FROM monitoring_acs")

data = cur.fetchall()

columns = [desc[0] for desc in cur.description]

df = pd.DataFrame(data, columns=columns)

cur.close()
conn.close()

if __name__ == '__main__':
    print(df.info(), end='\n\n\n')
    print(df.head())