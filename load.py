#!/usr/bin/python

import json
import sys
import maprdb

# the subset of the data we are loading -- actual will be min(DATA_SIZE, table size)
DATA_SIZE = 10000

# set this to the input json file for sensors
DATA_SENSORS_PATH = "/home/mapr/maprdb_python_examples/ws.json"

# set this to the input json file for maintenance
DATA_MAINT_PATH = "/home/mapr/maprdb_python_examples/maint.json"

# set these to the path in HDFS/MapR-FS where the table will live
TABLE_SENSORS_PATH = "/user/mapr/sdata"
TABLE_MAINT_PATH = "/user/mapr/mdata"

def open_db():
    print("opening db")
    return (maprdb.connect())

# create or get existing table
def open_table(connection, p):
    print("opening table %s" % p)
    if connection.exists(p):
        print("deleting old table %s" % p)
        connection.delete(p)
    return (connection.create(p))

i = 0
print("opening JSON file %s" % DATA_SENSORS_PATH)
db = open_db()
t = open_table(db, TABLE_SENSORS_PATH)

# first load the sensor data set
with open(DATA_SENSORS_PATH) as json_data:
    d = json.load(json_data)
    print("total points in file: %d" % len(d))
    print("total points to load: %d" % DATA_SIZE)
    for doc in d:
        i += 1
        if (i > DATA_SIZE):
             break
        sys.stdout.write('\r' + 'processing data point ' + str(i))
        inner = doc["sensor_readings"]
        newdoc = maprdb.Document(
            { '_id': str(doc["event_id"]),
              'sensor_readings.pressure': str(inner["pressure"]),
              'sensor_readings.temp': str(inner["temp"]),
              'sensor_readings.oil_percentage':
                  str(inner["oil_percentage"]),
              'hcid': str(doc["hcid"]),
              'timestamp': str(doc["timestamp"]),
              'production': str(doc["production"]),
              'injection_vol': str(doc["injection_vol"]) } )
        t.insert_or_replace(newdoc)
print(" ...done")
i = 0

# now load the maint. history data set
t = open_table(db, TABLE_MAINT_PATH)
print("opening JSON file %s" % DATA_MAINT_PATH)
with open(DATA_MAINT_PATH) as json_data:
    d = json.load(json_data)
    print("total points in file: %d" % len(d))
    print("total points to load: %d" % DATA_SIZE)
    for doc in d:
        i += 1
        if (i > DATA_SIZE):
             break
        sys.stdout.write('\r' + 'processing data point ' + str(i))
        newdoc = maprdb.Document({
              '_id': str(doc["event_id"]),
              'hcid': str(doc["hcid"]),
              'timestamp': str(doc["timestamp"]),
              'contractor': str(doc["contractor"]),
              'reason': str(doc["reason"]),

              # setting an array
              'actions_taken': doc["actions_taken"],
              'parts_serviced': doc["parts_serviced"],

              'parts_replaced': str(doc["parts_replaced"]),
              'job_hours': str(doc["job_hours"])})
        t.insert_or_replace(newdoc)
print(" ...done")
