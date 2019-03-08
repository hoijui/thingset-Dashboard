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

def out(msg):
    """ Print message on command line."""
    print(msg)
    sys.stdout.flush()

def connect_to(port):
    """Connect to serial port. Returns port instance."""
    try:
        ser = serial.Serial(port, 57600, timeout=10)
        ser.nonblocking()
        out("Listening on {} ..".format(port))
    except serial.SerialException:
        out("Error opening port {} .. aborting".format(port))
        sys.exit(1)

    return ser

def write_data(ser, c):
    while True:
        if ser.in_waiting > 0:
            raw_data = ser.readline()
            json_data = json.loads(raw_data.strip()[2:])
            data_frame = json_normalize(json_data)
            data_frame['time'] = datetime.now()
            data_frame.to_sql(name="Solarbox", con=c, if_exists='append')
            out("{}: data written to db.".format(data_frame.loc[0]['time']))

def main():
    """ This is the main function. Calls connect_to(port) and write_data(ser, c)"""
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="Serial port to listen to.")
    args = parser.parse_args()
    ser = connect_to(args.port)

    con = sqlite3.connect("data/solarbox.db")
    write_data(ser, con)


if __name__ == '__main__':
    main()
