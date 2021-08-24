#coding:utf-8

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import re
from elastic import elastic
import glob
import shutil
import os
import json
import pandas as pd

# function to add to JSON
def write_json(new_data, filename='data.json'):
    with open(filename,'a+') as file:
        json.dump(new_data, file, indent = 4)

def get_xml_element(file_xml, element):
    tree = ET.parse(file_xml)
    root = tree.getroot()
    if element == 'gp':
        return root.find("./md/mi/"+element)
    if element == 'mt':
        return root.findall("./md/mi/"+element)
    if element == 'mv':
        return root.findall("./md/mi/"+element)
    if element == 'ts':
        return root.find("./mff/"+element)
    if element == 'mts':
        return root.find("./md/mi/"+element)

def trait_moid_other(moid):
    dict_el = {} 
    moid = list(moid.text.split(','))
    node = re.sub(' ', '_', str(moid[0]).split('/')[0])
    node = re.sub(' ', '(', node)
    dict_el['Node'] = node
    dict_el['nodeType'] = str(moid[0]).split('/')[1].split(':')[0]
    dict_el['Object_Name_Type'] = str(moid[0]).split('/')[1].split(':')[1].split('=')[1]
    prop_ObjectName =  moid[1:len(moid)]
    for i, prop in enumerate(prop_ObjectName):
        prp = re.sub(' ', '_', prop).split('=')[1]
        dict_el["Prop_ObjectName_"+str(i)] = prp
        
    return dict_el;
    
def trait_moid(moid):
    moid = list(moid.text.split(','))
    info = []
    info.append(str(moid[0]).split('/')[0])
    info.append(str(moid[0]).split('/')[1].split(':')[0])
    info.append(str(moid[0]).split('/')[1].split(':')[1].split('=')[1])
    info.append(str(moid[1]).split('=')[1])
    return info 

def trait_mv(mv):
    info = []
    info.append(mv.find('moid'))
    info.append(mv.findall('r'))
    return info



def trait_mt(mt):
    mt_val = []
    for mt in mt:
        mt_val.append(mt.text)
    return mt_val

def trait_r(r):
    r_val = []
    for r in r:
        r_val.append(r.text)
    return r_val

def xml_to_dict(filename, cfg):
    name_file = os.path.basename(filename)
    mts = get_xml_element(filename, 'mts')
    mts = str(mts.text)
    hours=int(mts[8:10])
    minutes=int(mts[10:12])
    date = datetime(int(mts[0:4]), int(mts[4:6]), int(mts[6:8]), int(mts[8:10]), int(mts[10:12]))
    date = date.isoformat()
    gp = get_xml_element(filename, 'gp')
    mt = trait_mt(get_xml_element(filename, 'mt'))
    mv = get_xml_element(filename, 'mv')
    send_elastic = []
    dict_obj = {}
    for mv in mv:
        moid, r = trait_mv(mv)
        r = trait_r(r) 
        nullable = 'no'
        dict_obj = trait_moid_other(moid)
        for i in range(len(r)):
            if r[i] == 'NULL':
                r[i] = 0
                nullable == 'yes'

            mt[i] = re.sub(' ', '_', mt[i])
            dict_obj["counter_Name"] =  str(mt[i])
            dict_obj["date"] =  date
            dict_obj["counter_Value"] =  r[i]
            dict_obj["Nullable"] =  nullable
            dict_obj["filename"] =  name_file
            dict_obj['Period'] =  str(int(gp.text))

        
            json_object = json.dumps(dict_obj, indent = 4) 
            send_elastic += [json_object]
            converted_list = []
            converted_list.append(dict_obj)
            elastic.xml_to_elastic([dict_obj], cfg)
           
        


def read_from_multiple_xml(cfg, cfg_elastic):
    """Cette fonction cree un dataframe a partir de plusieur fichier
    
    Keyword arguments:path(le repertoir des fichier), sep(le caractere separateur),
    skiprows(la ou les ligne a ne pas considerer)
    Return: retourne un dataframe creer a partir de plusieur fichiers
    """
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    directory = [*cfg['xml'].values()]
    all_file = glob.glob(directory+'*')
    print(len(all_file))
    for filename in all_file:
        xml_to_dict(filename, cfg_elastic)
        os.remove(filename)
    print('*********Success!!!!!!!!!!!!!!!!!!!************')
