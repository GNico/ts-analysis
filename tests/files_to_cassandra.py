import numpy as np
import pandas as pd
import json
import os
import dateutil.parser
from datetime import datetime
import time
from cassandra.cluster import Cluster
from cassandra import util


# Script para escribir los archivos de las series en cassandra

seriesdates = []
series = {}
directory = os.path.join(os.getcwd(), 'data')
for filename in sorted(os.listdir(directory)):
    if not filename.endswith(".json"):
        continue
    with open(os.path.join(directory, filename)) as data_file:
        print("Processing " + str(data_file))
        data = json.load(data_file)
        for element in data:
            date = dateutil.parser.parse(element['source']['date'])
            date = time.mktime(date.timetuple())
            seriesdates.append(date)
            for tag in element['source']['tags']:
                if tag not in series:
                    series[tag] = []
                series[tag].append(date)



cluster = Cluster()
session = cluster.connect('db_tsa')
session.default_timeout = 3600

clientname = 'movi'
#guardando en cassandra la serie principal
series_name = clientname
for series_event_time in seriesdates:
    new_uuid = util.uuid_from_time(int(float(series_event_time)))
    session.execute("INSERT INTO time_series (name, event_time) VALUES (%s, %s)", (series_name, new_uuid))

#guardando las series de los tags
for tag_name, tag_series in series.items():
    series_name = clientname + '_' + tag_name
    for series_event_time in tag_series:
        new_uuid = util.uuid_from_time(int(float(series_event_time)))
        session.execute("INSERT INTO time_series (name, event_time) VALUES (%s, %s)", (series_name, new_uuid))


