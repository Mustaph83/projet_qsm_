#coding:utf-8
import argparse
import logging as lg
import yamale
import yaml
import os
from collect import collect
from parsing import 




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


def parse_arguments():
    arguments = argparse.ArgumentParser()
    arguments.add_argument("-cl", "--collectlocal", help=""" Pour collecter les fichier depuis un repertoire local
                            """)
    arguments.add_argument("-c", "--collect", help=""" Pour collecter(collect)
                            """)
    arguments.add_argument("-p", "--parsing", help=""" Pour parser(parsing)
                            """)
    return arguments.parse_args()



def main():
    args = parse_arguments()
    try:
        path = os.getcwd()
        collecter = args.collect
        parser = args.parsing
        if parser == None and collecter == None:
            raise Warning("Ils faut imperativement indiquer la methode a invoauer(deplyment, collcter, parser)")
    except Warning as e:
        lg.warning(e)
    else:
        config_path = os.path.join(path, 'config')
        if parser:
            config = os.path.join(config_path,'xml_config.yml')
            schema = os.path.join(config_path,'xml_schema.yml')
            cfg = validator_yaml(config, schema)
            config_el = os.path.join(config_path,'elastic_config.yml')
            schema_el = os.path.join(config_path,'elastic_schema.yml')
            cfg_elastic = validator_yaml(config_el, schema_el)
            parsing.read_from_multiple_xml(cfg, cfg_elastic)
        if collecter:
            config = os.path.join(config_path,'collect_config.yml')
            schema = os.path.join(config_path,'collect_schema.yml')
            cfg = validator_yaml(config, schema)
            collect.copy_files_from_remote(cfg)

if __name__ == '__main__':
    main()
