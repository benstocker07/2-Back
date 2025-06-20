import sqlite3
import time
from datetime import datetime

def create_db_connection():
    connection = sqlite3.connect('N-Back.db')
    create_table_if_not_exists(connection)
    return connection

def create_table_if_not_exists(connection):
    with connection:
        connection.execute("""
        CREATE TABLE IF NOT EXISTS triggers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trigger_code INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
        """)

def log_trigger(connection, trigger_code):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    with connection:
        connection.execute("INSERT INTO triggers (trigger_code, timestamp) VALUES (?, ?)", (trigger_code, current_time))

import pyxid2

devices = pyxid2.get_xid_devices()
global dev
dev = devices[0]

print(devices, dev)

global trigger_count
trigger_count = 0

db_connection = create_db_connection()

def test():
    dev.activate_line(lines=5)
    log_trigger(db_connection, 5)

def test1():
    dev.activate_line(lines=1)
    rttime = time.time()
    log_trigger(db_connection, 1)

def test2():
    dev.activate_line(lines=2)
    log_trigger(db_connection, 2)

def test3():
    dev.activate_line(lines=3)
    rttime = time.time()
    log_trigger(db_connection, 3)

def RT():
    dev.activate_line(lines=6)
    log_trigger(db_connection, 6)

def start():
    global trigger_count
    dev.activate_line(lines=7)
    log_trigger(db_connection, 7)

def stop():
    global trigger_count
    dev.activate_line(lines=8)
    log_trigger(db_connection, 8)

def split():
    global trigger_count
    dev.activate_line(bitmask=129)
    log_trigger(db_connection, "129")

def short():
    global trigger_count
    dev.activate_line(bitmask=100)
    log_trigger(db_connection, "100")

def intermediate():
    global trigger_count
    dev.activate_line(bitmask=101)
    log_trigger(db_connection, "101")

def long():
    global trigger_count
    dev.activate_line(bitmask=102)
    log_trigger(db_connection, "102")

def wrong():
    global trigger_count
    dev.activate_line(lines=4)
    log_trigger(db_connection, 4)

def close_connection():
    db_connection.close()

while True:
    trigger = int(input('Trigger: '))
    dev.activate_line(bitmask=trigger)
