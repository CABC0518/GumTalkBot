import psycopg2
import random
import os

class database:
    def __init__(self, server_table):
        PASSWORD = os.getenv("PASSWORD")
        DATABASE = os.getenv("DATABASE")
        self.server_table = server_table
        self._conn = psycopg2.connect(host="localhost", database=DATABASE, user="postgres", password=PASSWORD)
        self._cur = self._conn.cursor()

    def create_table(self):
        command = "CREATE TABLE IF NOT EXISTS {} ( id SERIAL PRIMARY KEY, topic VARCHAR(30) NOT NULL)".format(self.server_table)
        self._cur.execute(command)
        self._conn.commit()

# this function gets topics from default_topic.txt, inserts them into database
    def insert_default_topics(self):
        with open('default_topic.txt', 'r') as file:
            data = file.read()
            topics = data.split(",")
            for topic in topics:
                self.insert_topic(topic)

    def insert_topic(self, topic):
        command = "INSERT INTO {} (topic) VALUES ({})".format(self.server_table, topic)
        self._cur.execute(command)
        self._conn.commit()

    def remove_topic(self, topic):
        command = "DELETE FROM {} WHERE topic = {}".format(self.server_table, topic)
        self._cur.execute(command)
        self._conn.commit()

    def delete_all_topics(self):
        command = "DELETE FROM {}".format(self.server_table)
        self._cur.execute(command)
        self._conn.commit()

    def get_all_topics(self):
        topics = []
        command = "SELECT * FROM {}".format(self.server_table)
        self._cur.execute(command)
        result = self._cur.fetchall()
        for result in result:
            topics.append(result[1])
        return topics

# get all topics from database and creates 5 topics set and return it
    def get_topic_set(self):
        topics = self.get_all_topics()
        nums = random.sample(range(0, len(topics)), 5)
        topics_set = []
        for num in nums:
            topics_set.append(topics[num])
        print(topics_set)
        return topics_set
