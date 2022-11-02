import sqlite3
from datetime import datetime
import string

from typing import List


from application_settings import ApplicationSettings

settings = ApplicationSettings()
DB_FILE = settings.value("database_path")



def initDB():

    conn = sqlite3.connect(DB_FILE)

    cur = conn.cursor()
    cur.execute(''' CREATE TABLE IF NOT EXISTS sequences
        ( id INTEGER PRIMARY KEY AUTOINCREMENT,time_stamp real, data JSON )
    ''')

    conn.close()

def addItem(item):
    initDB()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    now = datetime.now()
    time_stamp = datetime.timestamp(now)
    cur.execute("INSERT INTO sequences values (NULL, ?,?)", 
        [time_stamp, item.toJSON()]
    )

    conn.commit()

    conn.close()

def readItems() -> List[any]:
    initDB()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()    
    cur.execute("SELECT * FROM sequences")

    rows = cur.fetchall()

    conn.close()
    jobs : List[any] = []

    for row in rows:

        db_id = row[0]
        time_stamp = row[1]
        json_str = row[2]
        # j  = Job()
        # j.fromJSON(json_str)
        # j.id = int(db_id)
        # j.time_stamp = time_stamp
        # jobs.append(j)

    return jobs

def deleteJob(id):
    initDB()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()    

    cur.execute("DELETE FROM jobs WHERE id=?", (id,))

    conn.commit()
    conn.close()

def updateJob(job : any):
    initDB()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()  
    json_string = job.toJSON()
    cur.execute("""UPDATE jobs SET data = ? where id = ?""", [json_string, job.id])

    conn.commit()

    conn.close()


