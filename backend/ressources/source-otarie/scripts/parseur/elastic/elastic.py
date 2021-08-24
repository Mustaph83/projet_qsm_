#coding:utf-8
from elasticsearch import Elasticsearch
import json
import logging as lg
from time import strptime
import pandas as pd
import datetime
import os 

def df_to_elastic(df, index):
    for data in df.to_dict(orient='records'):
        yield ('{ "index" : { "_index" : "%s" }}'% (index))
        yield (json.dumps(data, default=int))

def mapping_file(filepath):
    if os.path.isfile(filepath):
        with open(filepath, '+r') as f:
            data = json.load(f)
            return data
    else:
        return ''

def send_to_elastic(df, cfg):
    host, port, INDEX, TYPE, file_mapping = [*cfg['elastic'].values()]
    host = list(host.strip().split(','))
    print(host)
    es = Elasticsearch(host,port=port, sniff_on_start=True, timeout=200)
    #es = Elasticsearch(hosts=host,port=port, timeout=200)
    mapping = mapping_file(file_mapping)
    if es.indices.exists(index=INDEX):
        r = es.bulk(df_to_elastic(df, INDEX))
        print(not r['errors'])
    else:
        if mapping != '':
            es.indices.create(index=INDEX, body=mapping,ignore=[400, 404])
            r = es.bulk(df_to_elastic(df, INDEX))
            print(r['errors'])
        else:
            es.indices.create(index=INDEX, ignore=[400, 404])
            r = es.bulk(df_to_elastic(df, INDEX))
            print(r['errors'])
    
    
