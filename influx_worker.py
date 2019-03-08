import argparse,sys
import time
import serial
import json
from influxdb import InfluxDBClient

def out(msg):
    print(msg)
    sys.stdout.flush()

def connect_to_influx():
    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database('libresolar')
    return client


def serial_listen(portName, client):
    try:
        ser = serial.Serial(portName,57600, timeout=10)
        ser.nonblocking()
        out("Listening on {} ..".format(portName))
    except:
        out("Error opening port {} .. aborting".format(portName))
        sys.exit(1)
    
    while True:
        data = {}
        point = {"measurement": "Box1"}
        if (ser.in_waiting > 0):
            raw_data = ser.readline()
            json_data = json.loads(raw_data.decode('utf-8')[2:])
            point["fields"] = json_data
            data["points"] = [point]
            if client.write(data,{'db':'solarbox'}):
                out("Data point written in db.")
        time.sleep(0.01)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="Serial port device to listen to")
    args = parser.parse_args()
    portName = args.port

    client = connect_to_influx()    
    serial_listen(portName,client)


if (__name__ == '__main__'):
    main()