#!/usr/bin/env python
"""Dashboard for Libre Solar box. Reads data from sqlite database
and plots live data at http://localhost:8050"""

import sys
import threading
import argparse
import sqlite3
import time
from website.live_dashboard import create_app
from sqlite_worker import write_data, connect_serial

class dbThread(threading.Thread):
    def __init__(self, threadID, name, port, baud, table, f):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.port = port
        self.baud = baud
        self.table = table
        self.f = f
    def run(self):
        print("Starting " + self.name)
        ser = connect_serial(self.port, self.baud)
        con = sqlite3.connect(self.f)
        write_data(ser, con, self.table)
        print("Exiting " + self.name)

#class appThread (threading.Thread):
#    def __init__(self, threadID, name, app):
#        threading.Thread.__init__(self)
#        self.threadID = threadID
#        self.name = name
#        self.app = app
#    def run(self):
#        print ("Starting " + self.name)
#        self.app.run_server(debug=True)
#        print ("Exiting " + self.name)

def out(msg):
    """Print message on command line."""
    print(msg)
    sys.stdout.flush()

app = create_app()

if __name__ == '__main__':
    """This is the main function. Calls connect_serial(port, baud) and write_data(ser, dbcon, table)"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="Serial port to listen to (default: /dev/ttyACM0)", default="/dev/ttyACM0")
    parser.add_argument("--baud", help="Baud rate (default: 115200)", default="115200")
    parser.add_argument("--table", help="Name of the table in the database (default: ThingSet)", default="ThingSet")
    parser.add_argument("filename", help="Path to SQLite database file.")
    args = parser.parse_args()
    app.dbfile = args.filename

    thread = dbThread(1, "dbThread", args.port, args.baud, args.table, args.filename)
    #thread2 = appThread(2, "appThread", app)

    thread.start()
    time.sleep(5)
    app.run_server(debug=True)
    thread.join()
    print("Exiting main program")
