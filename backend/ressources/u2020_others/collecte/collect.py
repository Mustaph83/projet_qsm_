#coding:utf8
import yaml
import  paramiko
import scp
import sys
import logging as lg
import argparse
import re
from cerberus import Validator
import yamale
import datetime
import glob
import os
import shutil


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
        

def createSSHClient(server, port, user, password, ssh_key=None):
    """Function to return ssh client 
    
    Keyword arguments:
    argument -- server = @IP remote, port = port de connexion
                user=username, password=password remote, ssh_key= la cle ssh(s'il existe)
    Return: returne un client ssh
    """
    
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if ssh_key == None:
        client.connect(server, port, user, password)
        return client
    else:
        client.connect(server, port, user, ssh_key)
        return client


def progress(filename, size, sent):
    """Affiche la preogression du telechargement des fichier
    
    Keyword arguments:
    argument -- filename, size_file, sent
    """
    sys.stdout.write("%s's progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )


def copy_files_from_remote(cfg):
    """Copy files from remote server
    
    Keyword arguments:
    argument -- description
    Return: Successfull
    """
    
    connection_type, src_host, src_port,\
    src_username, src_password, ssh_key,\
    src_dir, date_var, formate, pattern_to_copy,\
    pattern_not_copy = [*cfg['source'].values()]

    dest_dir, u20_30 = [*cfg['destination'].values()]
    files_dest = os.listdir(dest_dir)
    pattern_to_copy = pattern_to_copy.strip()
    patterns = pattern_to_copy.split(',')
    for i, pattern in enumerate(patterns):
        patterns[i] = pattern.strip()
    if "date" in src_dir:
        if formate == '':
            raise Warning("Veuillez preciser le format de la date")
        if date_var == 'today':
            now = datetime.datetime.now()
            today00am = now.replace(hour=1, minute=0, second=0, microsecond=0)
            if now > today00am:
                d = datetime.date.today()
                date = d.strftime(formate)
                src_dir = re.sub('date',date, src_dir)
            else:
                d = datetime.date.today()
                d = d - datetime.timedelta(days=1)
                date = d.strftime(formate)
                src_dir = re.sub('date',date, src_dir)
        elif date_var == 'yesterday':
            d = datetime.date.today()
            d = d - datetime.timedelta(days=1)
            date = d.strftime(formate)
            src_dir = re.sub('date',date, src_dir)
        else:
            raise Warning('La date preciser n est pas valide date = today ou date = yesterday dans le fichier config' )
            exit(-1)
    if connection_type == 'ssh':
        if ssh_key == '':
            ssh = createSSHClient(src_host, src_port, src_username, src_password)
        else:
            ssh = createSSHClient(src_host, src_port, src_username, ssh_key)

        
        client = scp.SCPClient(ssh.get_transport(), progress=progress)
        sftp = ssh.open_sftp()
        rfiles = sftp.listdir(src_dir)
        for file in rfiles:
            if file in files_dest:
                continue
            if pattern_to_copy != '':
                for pattern in patterns:
                    if bool(re.match(pattern, file)):
                       if bool(re.match(pattern_not_copy, file)):
                          continue
                       else:
                           client.get(src_dir+file, dest_dir+''+file)
                           shutil.copy(dest_dir+file, u20_30+file)
                  
                else:
                    continue        
            else:
                client.get(src_dir+file, dest_dir+''+file)
        sftp.close
        ssh.close
    elif connection_type == 'ftp':
        transport = paramiko.Transport((src_host, src_port))
        transport.connect(username = src_username, password = src_password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        list_files = sftp.listdir(path=src_dir)
        for file in list_files:
            if file in files_dest:
                continue
            
            if pattern_to_copy != '':
                if bool(re.match(pattern_not_copy, file)):
                        continue
                for pattern in patterns:
                    if bool(re.match(pattern, file)):
                       if bool(re.match(pattern_not_copy, file)):
                           continue
    
                       else:
                          sftp.get(src_dir+file, dest_dir+''+file)
                          shutil.copy(dest_dir+file, u20_30+file)
                else:
                    continue  
                        
            else:
                sftp.get(src_dir+file, dest_dir+''+file)
        sftp.close()
        transport.close()
    else:
        raise Warning("Type of connection unreconnized!")

