# Introduction
```
 .d88888b. 888888        d8888 8888888 
d88P" "Y88b  "88b       d88888   888   
888     888   888      d88P888   888   
888     888   888     d88P 888   888   
888     888   888    d88P  888   888   
888     888   888   d88P   888   888   
Y88b. .d88P   88P  d8888888888   888   
 "Y88888P"    888 d88P     888 8888888     TM
            .d88P                      
          .d88P"                       
         888P"
```

This repo contains code examples for using python-bindings with JSON and MapR-DB (via the OJAI, Open JSON Application Interface).  Optionally, the code in the .py files posted here can be used to build a sample application with our partner, [Visual Action](http://www.visualaction.com/).  The HTML and Javascript files to build the full application are not present in this repo, but the complete JSON data flow can be built from these files and they serve as example reference code for getting started with OJAI and MapR-DB in Python.

# Prerequisites

### System Level Prerequisites

You must have a MapR-DB instance with OJAI running to use this example code.  Go to [maprdb.io](http://maprdb.io) to download the current developer snapshot, which consists of an easy-to-use virtual machine with all the software you need pre-installed.  This VM will give you a single-node Hadoop cluster running MapR.

### Python3 is Required

If you are using one of the MapR pre-supplied VMs, you may need to install ```python3```.  Future versions of the sandbox will contain this preinstalled.  To install ```python3``` on the sandbox, follow these steps:

1) As root, run:
```yum install zlib-devel```
```yum install openssl-devel```
2) [follow the steps outlined here](http://www.shayanderson.com/linux/install-python-3-on-centos-6-server.htm).  You will need to follow all these steps, including installing the "Development tools" group which takes a few minutes.  At the end of these steps you should be able to run ```python3 --version```

### Install the MapR-DB Python Package

To use Python with MapR-DB (as this example does), you will need the package [python-bindings](https://github.com/mapr-demos/python-bindings) installed.  You can install this by running ```pip3 install maprdb```.  

### Edit Variables and Prepare Files

The code examples that load data into MapR-DB do not require that the tables be made in advance, but they will delete the existing tables if they are there.  Edit ```load.py``` and change the variables TABLE_SENSORS_PATH and TABLE_MAINT_PATH to change the path of the tables.  These default to ```/user/mapr/mdata``` and ```/user/mapr/mdata```.

The data set used in this application is in this [wellsensors](https://github.com/namato/wellsensors) repo.  A small pair of datasets for the well and maintenance information (1M and 50K lines, respectively) is included in this repo.  To generate a larger dataset on your own, use the schema from the above repo with Ted Dunning's excellent [log-synth](https://github.com/tdunning/log-synth) tool to generate a set of arbitrary size.  Watch out, JSON can get big, fast!

Be sure to uncompress ```ws.json.gz``` and ```maint.json.gz``` before running the scripts.  If you are generating the graphs with ```makeplots.py```, edit the OUTPUT_PATH variable at the top of that file to set the output directory for the graph images.

# Using the Code Examples

The following files correspond to several code examples you can use to get familiar with how to load JSON into MapR-DB using Python.  

* ```load.py``` - reads each dataset (ws.json and maint.json), loads the JSON documents into MapR-DB
* ```makeplots.py``` - reads the data and makes a series of plots, using Spark.  This file can be executed in Spark by using ```spark-submit makeplots.py```.
* ```summary.py``` - reads the data outputs some summary statistics using a Pandas dataframe

These files are meant to be run in sequence, i.e. run ``load.py`` first, then either ``makeplots.py`` using the ``spark-submit`` command, or simply run ```summary.py``` with python3 and you can view basic statistics about the dataset.

# Additional Resources

[Follow the instructions in this video](https://www.youtube.com/watch?v=-pbvRTrJNIc) to build the application on your own machine.

Questions?  Visit the [maprdb.io](http://maprdb.io) page for more information and a support forum.
