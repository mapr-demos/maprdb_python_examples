#!/usr/bin/python
import json
import pandas as pd
import numpy as np
import sys
import pandas as pd
import datetime
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from dateutil import parser
from pyspark import SparkContext, SparkConf
import maprdb

# set this to the output path for the graphs
OUTPUT_PATH = "/home/mapr/vaweb/v2/graphs/"

# set this to the total N data points to read
DATA_SIZE = 10000

# set this to the path of the input table
TABLE_PATH = "/user/mapr/wdata"

def maprdb_get_table(path):
    print("opening table %s" % path)
    connection = maprdb.connect()
    return (connection.get(path))

def output_graph(name, e1, e2):
    names = []

    matplotlib.style.use('fivethirtyeight')
    matplotlib.rcParams.update({'font.size': 8})

    p = pd.DataFrame.plot(e1, \
        figsize=(16,4), subplots=True,
        style=['r','g','b','y','k'], sharex=True)
    p[0].legend(loc='upper right')
    p[1].legend(loc='upper right')
    p[2].legend(loc='upper right')
    filename = OUTPUT_PATH + \
        "bottom_" + name + ".png"
    plt.savefig(filename, transparent=True)
    names.append(filename)
    #print("outputting: %s" % filename)

    pd.DataFrame.plot(e2, y="Prod", figsize=(5,5))
    plt.locator_params(nbins=3)
    filename = OUTPUT_PATH + \
        "right_top_" + name + ".png"
    plt.savefig(filename, transparent=True)
    names.append(filename)
    #print("outputting: %s" % filename)

    filename = OUTPUT_PATH + \
        "right_bottom_" + name + ".png"
    pd.DataFrame.plot(e2, y="Inject Vol", figsize=(5,5))
    plt.locator_params(nbins=3)
    plt.savefig(filename, transparent=True)
    names.append(filename)
    #print("outputting: %s" % filename)

    plt.close('all')
    return (names)

# get time-series for each well into a data frame
# we have a top-level dict of wells
# the value for each dict entry is an array of Series, one for each column (temp, etc.)
# after this is done we create a dataframe for each well
def load_well_data_from_maprdb():
    print("reading well data")
    i = 0
    t = maprdb_get_table(TABLE_PATH)
    allwells = {}
    for item in t.find():
        i += 1
        if (i > DATA_SIZE):
            break
        thiswell = item["hcid"]
        wellent = [ [], [], [], [], [], [] ]
        if (thiswell in allwells):
            wellent = allwells[thiswell]

        # grab the values and the sensor sub-values
        wellent[0].append(item["timestamp"])
        wellent[1].append(int(item["sensor_readings"]["pressure"]))
        wellent[2].append(int(item["sensor_readings"]["temp"]))
        wellent[3].append(int(item["sensor_readings"]["oil_percentage"]))
        wellent[4].append(int(item["production"]))
        wellent[5].append(int(item["injection_vol"]))

        sys.stdout.write('\r' + \
            'Processing data point ' + str(i) + ' hcid ' + thiswell)
        allwells[thiswell] = wellent

    # make some pandas dataframes to compute the results
    print(" ...done")
    print("computing summaries")
    alldfs = []
    for w in allwells:
        cols = allwells[w]
        pdf1 = pd.DataFrame(
                { "Pressure" : cols[1],
                    "Temp" : cols[2],
                    "Oil Pct" : cols[3] },
                index=cols[0])
        pdf2 = pd.DataFrame(
                {
                    "Prod" : cols[4],
                    "Inject Vol" : cols[5] },
                index=cols[0])
        alldfs.append((w, pdf1, pdf2))
    return (alldfs)

print("writing graphs...")
sc = SparkContext()
s_rdd = sc.parallelize(load_well_data_from_maprdb())
fnames = s_rdd.map(lambda x: output_graph(x[0], x[1], x[2])).collect()

