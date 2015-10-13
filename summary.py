#!/usr/bin/python
import json
import pandas as pd
import numpy as np
import sys
import maprdb
from pprint import pprint

# set this to the total N data points to read
DATA_SIZE = 1000

# set this to the path of the input table
SENSOR_TABLE_PATH = "/user/mapr/sdata"

# set to hour for the query example
TIME_CUTOFF = 17

def maprdb_get_table(path):
    print("opening table %s" % path)
    connection = maprdb.connect()
    return (connection.get(path))

t_sensor = maprdb_get_table(SENSOR_TABLE_PATH)
sensordata = []
c = 0

for item in t_sensor.find():
    c += 1
    if (c > DATA_SIZE): break
    temp = int(item["sensor_readings"]["pressure"])
    pres = int(item["sensor_readings"]["temp"])
    oilp = int(item["sensor_readings"]["oil_percentage"])
    sensordata.append([temp, pres, oilp])

cols = ['pressure', 'temp', 'oil_percentage']
sds = pd.DataFrame(sensordata, columns=cols)

print("Overall Statistics")
print("------------------")
print("Mean:")
m = sds.mean()
for c in cols:
    print('\t' + c + ': %2.2f' % m[c])
print("Std. Dev:")
stdev = sds.std()
for c in cols:
    print('\t' + c + ': %2.2f' % stdev[c])
print("Variance:")
v = sds.var()
for c in cols:
    print('\t' + c + ': %2.2f' % v[c])
print("done")
