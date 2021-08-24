#coding:utf-8
from script_csv import parser_csv
import argparse
import logging as lg
import yamale
import yaml
import os


def parse_arguments():
    arguments = argparse.ArgumentParser()
    arguments.add_argument("-e", "--extension", help=""" Pour indiquer le type 
    de fichier""")
    return arguments.parse_args()

    
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

def main():
    args = parse_arguments()
    try:
        path = os.getcwd()
        extension = args.extension
        if extension == None:
            raise Warning("Ils faut imperativement indiquer les fichiers config et le schema de validations")
    except Warning as e:
        lg.warning(e)
    else:
        config = path+'/config/files_config.yml'
        schema = path+'/config/files_schema.yml'
        cfg = validator_yaml(config, schema)
        config_el = path+'/config/elastic_config.yml'
        schema_el = path+'/config/elastic_schema.yml'   
        cfg_elastic = validator_yaml(config_el, schema_el)
        parser_csv.read_from_multiple_csv(cfg, extension, cfg_elastic)


if __name__ == '__main__':
    main()
