import psycopg2

class database:

    def __init__(self, server_name):
        self.server_name = server_name
        self._conn = psycopg2.connect(host="localhost", database="test", user="postgres", password="lcac1965")
        self._cur = self._conn.cursor()

    def create_table(self):
        command = "CREATE TABLE IF NOT EXISTS {} ( id SERIAL PRIMARY KEY, topic VARCHAR(30) NOT NULL)".format(self.server_name)
        self._cur.execute(command)
        self._conn.commit()

    def insert_topic(self, topic):
        command = "INSERT INTO {} (topic) VALUES ({})".format(self.server_name, topic)
        self._cur.execute(command)
        self._conn.commit()
        print('topic succeessfully added')

    def remove_topic(self, topic):
        command = "DELETE FROM {} WHERE topic = {}".format(self.server_name, topic)
        self._cur.execute(command)
        self._conn.commit()
        print('topic succeessfully removed')

    def get_topics(self):
        topics = []
        command = "SELECT * FROM {}".format(self.server_name)
        self._cur.execute(command)
        result = self._cur.fetchall()
        for result in result:
            topics.append(result[1])
        return topics
