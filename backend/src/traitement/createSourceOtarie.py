#!/usr/bin/python3
#from sys import winver
import paramiko
import yaml
import os
import shutil
import ruamel.yaml
from yaml.loader import Loader


  
class ConfigFileOtarieS1():
    def __init__(self, info_config, info_deployment, elastic_config):
        self.info_config = info_config
        self.elastic = elastic_config
        self.sourcename = 'source-otarie'
        self.new_source = info_config['name']
        self.deployment_info = info_deployment
        self.ressource_dir = info_config['ressource_dir']
        print(self.sourcename)
        print(self.deployment_info)
    
    def get_path_source(self):
        listsource = os.listdir(self.ressource_dir)
        if self.sourcename in listsource:
            return os.path.join(self.ressource_dir, self.sourcename)
        else:
            raise Warning("Source not found")
            exit(-1)


    def get_path_script(self):
        return os.path.join(self.get_path_source(), 'scripts')
 
    def get_deployment_path(self):
        return self.deployment_info['deploymentPath']

    def get_path_new_source_from_deployment_server(self):
        return os.path.join(self.get_deployment_path(), self.new_source)

    def get_path_script_from_deployment_server(self):
        src = self.get_path_new_source_from_deployment_server()
        return os.path.join(src, 'scripts')

    def update_collecte_config_file(self):
        path_script = self.get_path_script()
        path_collect = os.path.join(path_script, 'collecte')
        path_collect_file = os.path.join(path_collect, 'config.yml')
        dirPath = os.path.join(self.get_path_new_source_from_deployment_server(), 'data')
        parse_dir = os.path.join(self.get_path_new_source_from_deployment_server(), 'parseDir')
        stream = open(path_collect_file, 'r')
        yaml = ruamel.yaml.YAML()
        yaml.indent(mapping=4, sequence=4, offset=2)
        yaml.preserve_quotes = True
        data = yaml.load(stream)
        data['source']['connection_type'] = self.info_config['accessMode']
        data['source']['host'] = self.info_config['ipAddress']
        data['source']['username'] = self.info_config['username']
        data['source']['password'] = self.info_config['password']
        data['source']['directory'] = self.info_config['path']
        data['source']['pattern_file'] = self.info_config['pattern']
        if self.info_config['date'] != '':
            data['source']['date'] = self.info_config['date']
            data['source']['format'] = self.info_config['format']
        data['destination']['directory'] = dirPath
        data['destination']['parse_dir'] = parse_dir

        with open(path_collect_file, 'w') as file:
            yaml.dump(data, file)
        
    def update_parsing_config_file(self):
        path_script = self.get_path_script()
        path_config = os.path.join(path_script, 'config')
        archdir = os.path.join(self.get_path_new_source_from_deployment_server(), 'archive')
        parsedir = os.path.join(self.get_path_new_source_from_deployment_server(), 'parseDir')
        path_parse_file = os.path.join(path_config, 'files_config.yml')
        stream = open(path_parse_file, 'r')
        yaml = ruamel.yaml.YAML()
        yaml.indent(mapping=4, sequence=4, offset=2)
        yaml.preserve_quotes = True
        data = yaml.load(stream)
        data['csv']['directory']= parsedir
        data['csv']['separateur']= self.info_config['separateur']
        data['csv']['column_to_convert'] = self.info_config['dateField']
        data['csv']['archive_directory'] = archdir

        with open(path_parse_file, 'w') as file:
            yaml.dump(data, file)


    def update_elastic_config_file(self):
        src_script = self.get_path_script_from_deployment_server()
        path_script = self.get_path_script()
        path_config = os.path.join(path_script, 'config')
        elastic_file = os.path.join(path_config, 'elastic_config.yml')
        config_dir_server = os.path.join(src_script, 'config')
        stream = open(elastic_file, 'r')
        yaml = ruamel.yaml.YAML()
        yaml.indent(mapping=4, sequence=4, offset=2)
        yaml.preserve_quotes = True
        data = yaml.load(stream)
        data['elastic']['host'] = self.elastic['hosts']
        data['elastic']['INDEX'] = self.info_config['indexName']
        data['elastic']['mapping'] = os.path.join(config_dir_server, 'mapping.json')
        
        with open(elastic_file, 'w') as file:
            yaml.dump(data, file)

    def create_new_source(self):
        src_dir = self.get_deployment_path()
        source_dir = self.get_path_source()
        ssh = paramiko.SSHClient()
        know_host = paramiko.AutoAddPolicy()
        ssh.set_missing_host_key_policy(know_host)
        ssh.connect(hostname=self.deployment_info['ipAddress'], port=22, username=self.deployment_info['username']\
             ,password=self.deployment_info['password'])
        #print(src_dir)
        #zip_file = os.path.join(self.script_dir, 'script')
        name = 'source' 
        shutil.make_archive(name, 'zip', source_dir)
        zip_file = name+'.zip'
        print('-----------------------------')
        print(zip_file)
        print(src_dir)
        ftp_client = ssh.open_sftp()
        des_dir = os.path.join(src_dir, 'source.zip')
        ftp_client.put(zip_file, des_dir)
        os.remove(zip_file)    
        ftp_client.close()
        new_path = os.path.join(src_dir, self.new_source)
        cmd = 'unzip '+des_dir+' -d '+new_path+' && rm '+des_dir
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        ssh.close()
    