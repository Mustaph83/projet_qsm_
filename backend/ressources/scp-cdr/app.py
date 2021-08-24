from deployment import deploy
import argparse
import logging as lg
from collect import get_files
import yamale
import yaml
import os
from parsing import cdr_scp

def parse_arguments():
    arguments = argparse.ArgumentParser()
    arguments.add_argument("-d", "--deployment", help=""" Pour deployer(deployment)
                            """)
    arguments.add_argument("-c", "--collect", help=""" Pour collecter(collect)
                            """)
    arguments.add_argument("-p", "--parsing", help=""" Pour parser(parsing)
                            """)
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
        all_dir = os.listdir(path)
        deployer = args.deployment
        collecter = args.collect
        parsers = args.parsing
        print(collecter)
        if deployer == None and parsers == None and collecter == None:
            raise Warning("Ils faut imperativement indiquer la methode a invoauer(deplyment, collcter, parser)")
    except Warning as e:
        lg.warning(e)
    else:
        if deployer:
            config_path = os.path.join(path, 'config')
            config = os.path.join(config_path, 'deploy_config.yml')
            schema = os.path.join(config_path, 'deploy_schema.yml')
            cfg = validator_yaml(config, schema)
            print(deploy.create_subfolder(cfg))
        elif collecter:
            config_path = os.path.join(path, 'config')
            config = os.path.join(config_path, 'collect_config.yml')
            schema = os.path.join(config_path, 'collect_schema.yml')
            cfg = validator_yaml(config, schema)
            get_files.copy_files_from_remote(cfg)
        elif parsers:
            config_path = os.path.join(path, 'config')
            config = os.path.join(config_path, 'parser_config.yml')
            schema = os.path.join(config_path, 'parser_schema.yml')
            config_el = os.path.join(config_path, 'elastic_config.yml')
            schema_el = os.path.join(config_path,'elastic_schema.yml')
            #cfg = validator_yaml(config, schema)
            cfg_elastic = validator_yaml(config_el, schema_el)
            #parser.read_from_multiple_csv(cfg, cfg_elastic)
            #config = r'/home/sgsn/in_vas/61/config.yml'
            #schema_f = r'/home/sgsn/in_vas/61/schema.yml'
            cfg = validator_yaml(config, schema)
            cdr_scp.read_from_multiple_csv(cfg, cfg_elastic)
            
        else:
            raise lg.error("Parametre non reconnue python app.py --help pour plus de detail")

if __name__ == '__main__':
    main()
