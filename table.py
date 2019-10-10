import sqlite3 as lite
import os
import sys

path = os.path.dirname(__file__) + "\\test.db"
conn = lite.connect(path, check_same_thread=False)
cur = conn.cursor()

with conn:
    cur.execute("CREATE TABLE User (id INT,name TEXT)")