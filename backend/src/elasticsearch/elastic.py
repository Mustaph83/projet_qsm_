from os import error
from typing import Sized
from sqlalchemy.sql.functions import percent_rank
from elasticsearch import Elasticsearch
import numpy as np
import pandas as pd
from datetime import datetime
import re


ES_HOST = '192.168.1.7'
PORT = 9200

def connect_elasticsearch():
    _es_obj = Elasticsearch(hosts=ES_HOST, port=PORT, timeout=200)
    if _es_obj.ping():
        print('Connect success')
    else:
        print('Not connected!!!')
    return _es_obj



def validate_iso8601(str_val):
    is_iso8601 = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]{1,3})?$').match
    try:            
        if is_iso8601( str_val ) is not None:
            return True
    except:
        pass
    return False

def searchall(kwards):    
    format_date = ['%d/%m/%Y %H:%M:%S', '%d-%m-%Y %H:%M:%S', '%d-%m-%Y %H%M%S','%d-%m-%Y %H-%M-%S',\
        '%d%m%Y %H:%M:%S', '%d/%m/%Y %H/%M/%S', '%d/%m/%Y %H%M%S',\
        '%Y/%m/%d %H:%M:%S','%Y-%m-%d %H:%M:%S','%Y%m%d %H:%M:%S']
    
    _es_obj = connect_elasticsearch()
    field = {}
    #_start = datetime.strptime(kwards['startTime'], '%d/%m/%Y %H:%M:%S').isoformat()
    #_stop = datetime.strptime(kwards['stopTime'], '%d/%m/%Y %H:%M:%S').isoformat()
    _start = None
    _stop = None
    if validate_iso8601(kwards['startTime']):
        _start = kwards['startTime']
        _stop = kwards['stopTime']
    
    else:
        for formater in format_date:
            try:
                datetime.strptime(kwards['startTime'], formater)
            except ValueError as e:
                continue
            else:
                _start = datetime.strptime(kwards['startTime'], formater).isoformat()
                _stop = datetime.strptime(kwards['stopTime'], formater).isoformat() 
    
    if not _start or not _stop:
        return f"{kwards['startTime']} or {kwards['stopTime']} is not reconized"
    query = {
            "query":{
                "range":{
                    "startTime":{
                        "gte":_start,
                        "lte":_stop
                    }
                }
            }
        }
    
    try:
        data = _es_obj.search(index=kwards['index'],body=query, size=5000)
    except TypeError:
        return pd.DataFrame({})
    else:
        df = query_to_df(data)
        return df


def searchOne(kwards):
    _es_obj = connect_elasticsearch()
    field = {}
    
    format_date = ['%d/%m/%Y %H:%M:%S', '%d-%m-%Y %H:%M:%S', '%d%m%Y %H:%M:%S', \
        '%Y/%m/%d %H:%M:%S','%Y-%m-%d %H:%M:%S','%Y%m%d %H:%M:%S']
    
    is_iso8601 = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]{1,3})?$').match
    _number = kwards['number']
    
    if validate_iso8601(kwards['startTime']):
        _start = kwards['startTime']
        _stop = kwards['stopTime']
    else:
        for formater in format_date:
            try:
                datetime.strptime(kwards['startTime'], formater)
            except ValueError as e:
                continue
            else:
                _start = datetime.strptime(kwards['startTime'], formater).isoformat()
    
                _stop = datetime.strptime(kwards['stopTime'], formater).isoformat()
    
    query ={
            "query": {
                "bool": {
                "must": [{
                    "term": {
                        "cust":_number 
                    }
                    },
                    {
                    "range": {
                        "startTime": {
                        "gte": _start,
                        "lt": _stop
                        }
                    }
                    }
                ]
                }
            }
        }
    try:
        data = _es_obj.search(index=kwards['index'],body=query, size=5000)
    except TypeError:
        return pd.DataFrame({})
    else:
        df = query_to_df(data)
        return df

def query_to_df(data):
    field = {}
    list_df = []
    for doc in data['hits']['hits']:
        source_data = doc['_source']
        for key, valu in source_data.items():
            try:
                field[key] = np.append(field[key], valu)
            except KeyError as e:
                field[key] = np.array([valu])
        
    df = pd.DataFrame(field)
    df['nBytesUp+nBytesDn'] = df['nBytesUp']+df['nBytesDn']
    print(df['nBytesUp+nBytesDn'])
    return df