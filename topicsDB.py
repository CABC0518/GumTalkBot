#!/usr/bin/python
import psycopg2
# from config import config

def create_table():
    table_name = "discord_{server_id}"
    sql = 'INSERT INTO server_list VALUES {table_name}'
    cur.execute("CREATE TABLE IF NOT EXISTS topics (id INT NOT NULL PRIMARY KEY, topic VARCHAR(20))")

def connect():
    """ Connect to the PostgreSQL database server """
    conn = psycopg2.connect(
    host="localhost",
    database="test",
    user="postgres",
    password="lcac1965")
    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        # conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()
        server_name = 'server_132413443'

	# execute a statement
        command = "SELECT topic FROM {}".format(server_name)
        cur.execute(command)
        conn.commit()

        result = cur.fetchall();
        print(result)

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
