import pandas as pd
import json
import gzip
import os
import glob
from elasticsearch import Elasticsearch


def return_dataframe(filepath, sep=None, skiprows = 1):
    """Cette fonction return un dataframe pandas a partir d'un fichier
    
    Keyword arguments:filepath(le chemin du fichier),sep(le caracter separateur)
    skiprows(la ou les ligne a ne pas considerer) 
    Return: retourn un dataframe a partir d'un fichier
    """
    if filepath.endswith('.gz'):
        file_unzip = unzip_file(filepath)
        if skiprows != 1:
            dataframe = pd.read_csv(file_unzip, skiprows=skiprows, sep=sep, engine='python')
        else:
            dataframe = pd.read_csv(file_unzip, skiprows=skiprows, sep=sep, engine='python', header=None)
    else:
        if skiprows != 1:
            dataframe = pd.read_csv(filepath, skiprows=skiprows, sep=sep, engine='python')
        else:
            dataframe = pd.read_csv(filepath, skiprows=skiprows, sep=sep, engine='python', header=None)
    return dataframe


def read_from_multiple_csv(path, sep, skiprows):
    """Cette fonction cree un dataframe a partir de plusieur fichier
    
    Keyword arguments:path(le repertoir des fichier), sep(le caractere separateur),
    skiprows(la ou les ligne a ne pas considerer)
    Return: retourne un dataframe creer a partir de plusieur fichiers
    """
    
    all_file = glob.glob(path+'/*')
    print(len(all_file))
    list_df = []
    for filename in all_file:
        if filename.endswith('.gz'):
            file_unzip = unzip_file(filename)
            df = return_dataframe(file_unzip, sep, skiprows)
            list_df.append(df)
        else:
            df = return_dataframe(filename, sep, skiprows)
            list_df.append(df)
     
    frame = pd.concat(list_df, axis=0, ignore_index=True)
    print(frame)
    return frame


def unzip_file(filepath):
    """Cette fonction permet de decompresser des fichiers .gz
    
    Keyword arguments: flepath(le fichier compresser)
    argument -- description
    Return: retourne un fichier descompresser
    """
    
    with open(filepath, 'rb') as file:
        unzip_file = gzip.GzipFile(fileobj=file)
    return unzip_file
    

def sub_dataframe(dataframe, indexs, headers):
    """Cette fonction un sous dataframe a partir d'un dataframe
    
    Keyword arguments: dataframe(le dataframe)
    Return: returne un sous dataframe
    """
    if indexs == None or headers == None:
        raise Warning("il faut donner les indexs des colonnes")
    list_name = headers.split(',')
    params = [int(i) for i in indexs.split(',')]
    sub_data = dataframe.iloc[:,[i for i in params] ]
    sub_data.columns = [name for name in list_name]
    print(sub_data.head(5))
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

INDEX = 'IN/VAS'
TYPE = 'index'        
def rec_to_action(df):
    for index in df.to_dict(orient='index'):
        yield ('{ "index" : { "_index" : "%s", "_type" : "%s" }}'% (INDEX, TYPE))
        yield (json.dumps(index, default=int))


def send_to_elastic(df):
    e = Elasticsearch(hosts='192')
    if not e.indices.exists(INDEX):
        raise RuntimeError('index does not exists, use `curl -X PUT \
                            "localhost:9200/%s"` and try again'%INDEX)
    r = e.bulk(rec_to_action(df))
    print(not r['errors'])


