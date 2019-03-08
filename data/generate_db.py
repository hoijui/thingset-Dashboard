import argparse
import json
import sqlite3
from pandas.io.json import json_normalize

def file_to_sqlite(fname):
    with open(fname) as f:
        raw_data = f.readlines()

    raw_data = [json.loads(line.strip()[2:]) for line in raw_data]
    df = json_normalize(raw_data)
    print("Detected {} rows and {} columns.".format(len(df),len(df.columns)))

    con = sqlite3.connect("solarbox.db")
    df.to_sql(name="Solarbox", con=con)
    print("solarbox.db written.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="ThingSet data file (raw serial data).")
    args = parser.parse_args()
    fname = args.file

    file_to_sqlite(fname)

if (__name__ == '__main__'):
    main()