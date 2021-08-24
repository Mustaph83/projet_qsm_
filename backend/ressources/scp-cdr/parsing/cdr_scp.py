import pandas as pd
import json
import gzip
import os
import glob
from elastic import elastic
import yamale
import yaml
import datetime
import re
import math


def validator_yaml(yaml_file, schema_file):
    """Cette fonction permet de v
    alider un fichier yaml
    
    Keyword arguments: cfg : le yaml, schema: le validator
    Return: returne yaml or error
    """
    data = yamale.make_data(yaml_file)
    schema = yamale.make_schema(schema_file)
    try:
        yamale.validate(schema, data)
    except ValueError as e:
        print('Validation failed!\n%s' % str(e))
    else:
        with open(r''+yaml_file, 'r') as config_file:
            try:
                return yaml.load(config_file, Loader=yaml.FullLoader)
            except yaml.YAMLError as error:
                raise error

def gen_map(df, file, date_field):
    with open(file, '+r') as f:
        json_ob = json.load(f)
        for column in df.columns:
            if column in date_field:
                column = {
                            "type":"date"
                        }
            else:
                json_obj['mappings']['properties']['column']= {
                        "type":"keyword"
                    }
        f.write(json_ob) 

'''def controller_call(cfg, cfg_elastic):
    json_ob =  {
    "mappings":{
        "properties":{
        }
     }
    }
    path = cfg['in'].get('path') 
    list_dir = os.listdir(path)
    for dir in list_dir:
        if os.path.isdir(dir) & dir.startswith('SMC'):
            path_file = os.path.join(path, dir)
            config = os.path.join(path_file, 'config.yml')
            schema_f = os.path.join(path_file, 'schema.yml')
            mapping  = os.path.join(path_file, 'mapping.json')
            cfg = validator_yaml(config, schema_f)
            if cfg == None:
                continue
            else:
                read_from_multiple_csv(cfg, cfg_elastic)
    return "successs!!!"'''


def return_dataframe(filepath, sep=None, skiprows = 1, chunksize = None):
    """Cette fonction return un dataframe pandas a partir d'un fichier
    
    Keyword arguments:filepath(le chemin du fichier),sep(le caracter separateur)
    skiprows(la ou les ligne a ne pas considerer) 
    Return: retourn un dataframe a partir d'un fichier
    """
    if filepath.endswith('.gz'):
        file_unzip = unzip_file(filepath)
        if skiprows != 1:
            dataframe = pd.read_csv(file_unzip, skiprows=skiprows, sep=sep, chunksize=chunksize)
        else:
            dataframe = pd.read_csv(file_unzip, skiprows=skiprows, sep=sep, chunksize=chunksize, header=None)
    else:
        if skiprows != 1:
            dataframe = pd.read_csv(filepath, skiprows=skiprows, sep=sep, chunksize=chunksize)
        else:
            dataframe = pd.read_csv(filepath, skiprows=skiprows, sep=sep, chunksize=chunksize, header=None,  error_bad_lines=False)
    return dataframe


def read_from_multiple_csv(cfg, cfg_el):
    """Cette fonction cree un dataframe a partir de plusieur fichier
    
    Keyword arguments:path(le repertoir des fichier), sep(le caractere separateur),
    skiprows(la ou les ligne a ne pas considerer)
    Return: retourne un dataframe creer a partir de plusieur fichiers
    """
    path, sep, skiprows, chunksize, index, index_name, date_field, format_list  = [*cfg['in'].values()]
    index_name = index_name.split(',')
    for i,name in enumerate(index_name):
        index_name[i] = index_name[i].strip().replace(' ','_')
    format_list = format_list.split(',') 
    all_file = os.listdir(path)
    list_df = []
    for filename in all_file:
        #f = r'C:\Users\stg_mbaye56279\Documents\in_vas\config\mapping.json'
        filename = os.path.join(path,filename)
        if filename.endswith('.gz'):
            file_unzip = unzip_file(filename)
            df = return_dataframe(file_unzip, sep, skiprows, chunksize)
            for chunk in df:
                sub_df = sub_dataframe(chunk, index, index_name, cfg_el, format_list, date_field)
                #elastic.send_to_elastic(sub_df, cfg_el)
                
        else:
            df = return_dataframe(filename, sep, skiprows, chunksize)
            for chunk in df:
                #gen_map(chunk, f, date_field)
                sub_df = sub_dataframe(chunk, index, index_name,cfg_el, format_list, date_field)
                #elastic.send_to_elastic(sub_df, cfg_el)
    return 'successss!!'


def unzip_file(filepath):
    """Cette fonction permet de decompresser des fichiers .gz
    
    Keyword arguments: flepath(le fichier compresser)
    argument -- description
    Return: retourne un fichier descompresser
    """
    
    with open(filepath, 'rb') as file:
        unzip_file = gzip.GzipFile(fileobj=file)
    return unzip_file

def validate_date(date_text, list_format):
    try: 
       for formater in list_format:
           if bool(datetime.datetime.strptime(str(date_text), str(formater))):
                  return formater
           else:
                continue
    except ValueError:
            return ''
           

def sub_dataframe(dataframe, indexs, headers, cfg_el, format_list=None, date_field=None):
    """Cette fonction un sous dataframe a partir d'un dataframe
    
    Keyword arguments: dataframe(le dataframe)
    Return: returne un sous dataframe
    """
    headers = [elem.strip() for elem in headers]
    header = [elem.strip().replace(' ','_') for elem in headers] 
    dataframe = dataframe.fillna(0)
    #print(dataframe)
    if indexs == None or headers == None:
        raise Warning("il faut donner les indexs des colonnes")
    params = [int(i) for i in indexs.split(',')]
    for i,frm in enumerate(format_list):
        format_list[i] = frm.strip()

    sub_data = dataframe.iloc[:,[i for i in params] ]
    sub_data.columns = [name.strip() for name in headers]
    for column in sub_data.columns:
        print(column) 
        print(sub_data[column])
    if date_field !=  None or date_field != '':
        converts = list(date_field.split(','))
        for field in converts:
            field = field.strip().replace(' ','_')
            if field in sub_data.columns:
               indexs = sub_data[field].loc[lambda x: pd.isna(x)].index
               print(indexs.values)
               if len(indexs.values) > 0:
                  for i in indexs.values:
                      sub_data[field][i] = sub_data[field].iloc[i-1]
                  print(sub_data[field])
               indexs = sub_data[field].loc[lambda x: pd.isna(x)].index
               if len(sub_data[field].tolist()) <= 1: 
                     date_text = sub_data[field].iloc[0]
               else:
                     date_text = sub_data[field].iloc[1]
               formater = validate_date(date_text, format_list)
               #print(type((formater))
               if formater == '':
                  if bool(re.match('^[0-9]+\.[0-9]+\.[0-9]+ [0-9]+:[0-9]+:[0-9]+$',str(date_text))):
                     indexs = sub_data[field].loc[lambda x: pd.isna(x)].index
                     print(sub_data[field])
                     print(sub_data[field])
                     sub_data[field] = sub_data[field].map(lambda x: datetime.datetime.strptime(str(x).replace('.','-'), "%Y-%m-%d %H:%M:%S"))
                     sub_data[field] = sub_data[field].map(lambda x: x.isoformat())
                     print(sub_data[field])
                     #elastic.send_to_elastic(sub_data, cfg_el)
                  else:
                       print(sub_data)
                       #print(date_text)
                       raise Warning("Ce format n'est pas reconnu") 
               else:
                  
                  sub_data[field] = sub_data[field].map(lambda x: datetime.datetime.strptime(str(x), formater))
                  sub_data[field] = sub_data[field].map(lambda x: x.isoformat())
                  #elastic.send_to_elastic(sub_data, cfg_el)
                  print(sub_data)
                  print(sub_data[field])
            else:
              raise Warning('Le fichier ne contient pas de colonne '+field)

    return sub_data


def datafreme_to_json(data):
    """Convertis un dataframe sous un format json
    
    Keyword arguments: data(dataframe)
    """
    data_json = data.to_json(orient="index")
    with open(r'/home/mustaph/Documents/projet_QSM/data/file.json', 'a+') as file:
        parsed = json.loads(data_json)
        file.write(json.dumps(parsed, indent=4))


def create_dataframe(filepath, sep=None, skiprows = 1):
    """Creer un ou des dataframes a partir du parametetre filepath
    
    Keyword arguments: filepath(un fichier ou un repertoir)
    Return: returne un dataframe
    """
    
    os.path.isfile(filepath)
    if os.path.isfile(filepath):
        datframe = return_dataframe(filepath, sep, skiprows)
    elif os.path.isdir(filepath):
        dataframe = read_from_multiple_csv(filepath, sep, skiprows)
    else:
        raise Warning(f'type of {filepath} undifined')
    #print(dataframe.head(2))
    return dataframe
        
