#!/usr/bin/env python

"""Listen on serial port for ThingSet data and write data into
sqlite database"""

import sys
import argparse
import sqlite3
import json
from datetime import datetime
import serial
from pandas.io.json import json_normalize
import time

def out(msg):
    """Print message on command line."""
    print(msg)
    sys.stdout.flush()

def connect_serial(port, baud):
    """Connect to serial port. Returns port instance."""
    try:
        ser = serial.Serial(port, baud, timeout=10)
        ser.nonblocking()
        out("Listening on {} ..".format(port))
    except serial.SerialException:
        out("Error opening port {} .. aborting".format(port))
        sys.exit(1)

    return ser

def write_data(ser, dbcon, table):
    while True:
        if ser.in_waiting > 0:
            try:
                raw_data = ser.readline()
                if raw_data[0:2] == b'# ':
                    json_data = json.loads(raw_data.strip()[2:])
                    data_frame = json_normalize(json_data)
                    data_frame['time'] = datetime.now()
                    data_frame.to_sql(name=table, con=dbcon, if_exists='append')
                    out("{}: data written to db.".format(data_frame.loc[0]['time']))
            except json.decoder.JSONDecodeError as e:
                pass
        time.sleep(0.1)

def main():
    """This is the main function. Calls connect_serial(port, baud) and write_data(ser, dbcon, table)"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="Serial port to listen to (default: /dev/ttyACM0)", default="/dev/ttyACM0")
    parser.add_argument("--baud",help="Baud rate (default: 115200)", default="115200")
    parser.add_argument("--table",help="Name of the table in the database (default: ThingSet)", default="ThingSet")
    parser.add_argument("filename", help="Path to SQLite database file.")
    args = parser.parse_args()

    ser = connect_serial(args.port, args.baud)
    con = sqlite3.connect(args.filename)
    write_data(ser, con, args.table)


if __name__ == '__main__':
    main()
