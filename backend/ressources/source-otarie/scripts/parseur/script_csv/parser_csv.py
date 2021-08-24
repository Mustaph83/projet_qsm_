#coding-utf-8

"""
    Ce fichier est pour parser les fichier Txt/csv
    issus de la source otarie 
"""
import gzip
import glob
import pandas as pd
import yamale
import yaml
from elastic import elastic
import datetime
import shutil

import os

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



def unzip_file(filepath):
    """Cette fonction permet de decompresser des fichiers .gz
    
    Keyword arguments: flepath(le fichier compresser)
    argument -- description
    Return: retourne un fichier descompresser
    """
    
    with open(filepath, '+rb') as file:
        unzip_file = gzip.GzipFile(fileobj=file)
    return unzip_file

    

def return_dataframe(filename, sep):
    """Cette fonction return un dataframe pandas a partir d'un fichier
    
    Keyword arguments:filepath(le chemin du fichier),sep(le caracter separateur)
    skiprows(la ou les ligne a ne pas considerer) 
    Return: retourn un dataframe a partir d'un fichier
    """
    dataframe = pd.read_csv(filename, sep=sep, compression='gzip', dtype=str)
    return dataframe

def read_file_by_chunk(filename, sep, chunksize, cfg, convert=''):
    data = pd.read_csv(filename, sep=sep, chunksize=chunksize, compression='gzip')
    if convert != '':
        converts = list(convert.split(','))
        for chunk in data:
            for field in converts:
                if field in chunk.columns:
                    chunk[field] = chunk[field].map(lambda x: datetime.datetime.fromtimestamp(x).isoformat())
                    print(chunk[field])
                else:
                    raise Warning('Le fichier ne contient pas de colonne '+field)
                
            elastic.send_to_elastic(chunk, cfg)
    elif convert == '':
        for chunk in data:
            print(chunk)
            elastic.send_to_elastic(chunk, cfg)
    else:
        raise Warning("Le champs colum_to_convert dans le fichier config doit etre une string ou une chaine vide")
        
        
        

def read_from_multiple_csv(cfg, extension, cfg_elastic):
    """Cette fonction cree un dataframe a partir de plusieur fichier
    
    Keyword arguments:path(le repertoir des fichier), sep(le caractere separateur),
    skiprows(la ou les ligne a ne pas considerer)
    Return: retourne un dataframe creer a partir de plusieur fichiers
    """
    if extension == 'csv':
        host, port, username, password, pattern, sep, chunksize, fild_to_convert, directory, dir_arch = [*cfg['csv'].values()]
        all_file = glob.glob(directory+'*')
        print(directory)
        print(len(all_file))
        for filename in all_file:
            print(filename)
            if chunksize != None:
                read_file_by_chunk(filename, sep, chunksize, cfg_elastic, fild_to_convert)
                os.remove(filename)
            else:
                df = return_dataframe(filename, sep)
                elastic.send_to_elastic(df, cfg_elastic)
            #shutil.move(file, dir_arch)
    elif extension == 'xml':
        print('Wait comming next')
    else:
        raise Warning('this ext not reconize')
    print('*********Success!!!!!!!!!!!!!!!!!!!************')
    
