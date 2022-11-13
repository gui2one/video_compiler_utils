import sqlite3
from datetime import datetime
import string
import json
from typing import List


from application_settings import ApplicationSettings
from widgets.ImageSequenceItem import ImageSequenceItem
settings = ApplicationSettings()
DB_FILE = settings.value("database_path")



def initDB():

    conn = sqlite3.connect(DB_FILE)

    cur = conn.cursor()
    cur.execute(''' CREATE TABLE IF NOT EXISTS sequences
        ( id INTEGER PRIMARY KEY AUTOINCREMENT,time_stamp real, data JSON )
    ''')

    conn.close()

def addItem(item : ImageSequenceItem):
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
    items : List[ImageSequenceItem] = []

    for row in rows:

        db_id = int(row[0])
        time_stamp = float(row[1])
        json_str = row[2]
        # print(json_str)
        json_data = json.loads(json_str)
        j  = ImageSequenceItem(json_data["root_dir"], json_data["file_pattern"], db_id)
        j.fromJSON(json_data)
        j.id = int(db_id)
        j.time_stamp = time_stamp
        print(json_data)
        items.append(j)

    return items

def deleteItem(id: int):
    initDB()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()    

    cur.execute("DELETE FROM sequences WHERE id=?", (id,))

    conn.commit()
    conn.close()


def updateItem(seq : ImageSequenceItem):
    initDB()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()  
    json_string = seq.toJSON()
    cur.execute("""UPDATE sequences SET data = ? where id = ?""", [json_string, seq.id])

    conn.commit()

    conn.close()


