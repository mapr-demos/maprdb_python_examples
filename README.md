# maprdb_python_examples
This repo contains code for using python-bindings with JSON and MapR-DB.  The code in the .py files posted here is used to build a sample application with our partner, [Visual Action](http://www.visualaction.com/).

# Prerequisites

You must have a MapR-DB instance with OJAI running to use this example code.  Go to [maprdb.io](http://maprdb.io) to download the current developer snapshot, which consists of an easy-to-use virtual machine with all the software you need pre-installed.  This VM will give you a single-node Hadoop cluster running MapR.

To use Python with MapR-DB (as this example does), you will need the package [python-bindings](https://github.com/mapr-demos/python-bindings) installed.  You can install this by running ```pip install maprdb```.  Python3 is required.

The code examples that load data into MapR-DB do not require that the tables be made in advance, but they will delete the existing tables if they are there.  Edit ```load.py``` and change the variables TABLE_SENSORS_PATH and TABLE_MAINT_PATH to change the path of the tables.  These default to ```/user/mapr/mdata``` and ```/user/mapr/mdata```.

The data set used in this application is in this [wellsensors](https://github.com/namato/wellsensors) repo.  A small pair of datasets for the well and maintenance information (1M and 50K lines, respectively) is included in this repo.  To generate a larger dataset on your own, use the schema from the above repo with Ted Dunning's excellent [log-synth](https://github.com/tdunning/log-synth) tool to generate a set of arbitrary size.  Watch out, JSON can get big, fast!

Be sure to uncompress ```ws.json.gz``` and ```maint.json.gz``` before running the scripts.  If you are generating the graphs with ```makeplots.py```, edit the OUTPUT_PATH variable at the top of that file to set the output directory for the graph images.

# Code Examples in This Repo

The following files correspond to several code examples you can use to get familiar with how to load JSON into MapR-DB using Python.  

* ```load.py``` - reads each dataset (ws.json and maint.json), loads the JSON documents into MapR-DB
* ```makeplots.py``` - reads the data and makes a series of plots, using Spark.  This file can be executed in Spark by using ```spark-submit makeplots.py```.
* ```summary.py``` - reads the data outputs some summary statistics using a Pandas dataframe

These files are meant to be run in sequence, i.e. run ``load.py`` first, then either ``makeplots.py`` using the ``spark-submit`` command, or simply run ```summary.py``` with python3 and you can view basic statistics about the dataset.

# Additional Resources

[Follow the instructions in this video](https://www.youtube.com/watch?v=-pbvRTrJNIc) to build the application on your own machine.

Questions?  Visit the [maprdb.io](http://maprdb.io) page for more information and a support forum.
