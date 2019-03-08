#!/usr/bin/env python
""" This script parses raw ThingSet data from a file
and sends it to a given serial port every 1 second."""

import argparse
import time
import serial

def main():
    """Open serial port, read lines from raw_data.txt and send it to serial port."""
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="Serial port to stream data to")
    args = parser.parse_args()

    port_name = args.port

    with open('data/raw_data.txt') as f:
        raw_data = f.readlines()

    ser = serial.Serial()
    ser.baudrate = 57600
    ser.port = port_name
    ser.open()

    for line in raw_data:
        ser.write(line.encode('utf-8'))
        print("Sent line.")
        time.sleep(1)


if __name__ == '__main__':
    main()
