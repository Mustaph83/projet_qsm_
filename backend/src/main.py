# coding:utf-8
from datetime import date
from sqlalchemy.sql.schema import DefaultClause
from .entities.u2020Others import U2020Others, U2020OthersSchema
import secrets

from sqlalchemy.sql.expression import delete
from sqlalchemy.sql.selectable import HasSuffixes
from .entities.user import User, UserSchema
from os import error, name, path
from flask.globals import session
from flask_cors import CORS
from flask import Flask, json, jsonify, request
from sqlalchemy import select,update, delete
from .entities.entity import Session, engine, Base
from .entities.search import SearchSchema
from .entities.source import Source, SourceSchema
from .entities.host import Host, HostSchema
from .entities.script import Script, ScriptSchema
from .entities.otarie import Otarie, OtarieSchema
from .traitement import source
from .entities.sourcein import SourceIn, SourceInSchema
import jwt
import secrets
from .elasticsearch import elastic
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

secret_key = secrets.token_hex(16)
# generate database schema
# creating the Flask application




app = Flask(__name__)
CORS(app)
app.config.from_pyfile('config.py')
Base.metadata.create_all(engine)
#app.config.from_pyfile('config.py')
# start session
#session = Session()

# check for existing data



#host = session.query(Host).all()
#source = session.query(Source).all()

@app.route('/user', methods=['POST', 'GET', 'PUT'])
def get_post_put_user():
    session = Session()
    if request.method == 'GET':
        print(secrets.token_hex(16))
        user_obj = session.query(User).all()
        schema = UserSchema(many=True)
        users = schema.dump(user_obj)
        session.close()
        return jsonify(users), 200
    if request.method == 'POST':
        posted_user = UserSchema(only=('username', 'password', 'profil', 'email')).load(request.get_json())
        print(posted_user)
        user = User("HTTP post request", posted_user)
        user_exist = session.execute(select(User.username, User.password)\
            .where(User.username == posted_user['username'],\
                User.password == posted_user['password']), User.profil == posted_user['profil']).first()
        if user_exist == None:
            session = Session()
            session.add(user)
            session.commit()
            message = {}
            message['message'] = 'Request sucess'
            return jsonify(message), 201
        else:
            error = {}
            error['message'] = "this user exist"
            return jsonify(error),301
    if request.method == 'PUT':
        body = UserSchema(only=('id','username', 'password', 'profil', 'email'))\
            .load(request.get_json())
        user = session.execute(select(User).where(User.id == body['id'])).first()
        if user == None:
            error = {}
            error['message'] = 'User Not Found'
            return jsonify(error), 201

        session.execute(update(User).where(User.id==body['id']).values(username=body['username'],\
            password=body['password'], profil=body['profil'], email=body['email']))
        session.commit()
        session.close()
        feedback = {}
        feedback['message'] = 'statu user'+str(body['id'])+'is updated from postgresql'
        return jsonify(feedback), 201
    

@app.route('/user/<id>', methods=['GET', 'DELETE'])
def edit_get_remove_user_by_id(id):
    session = Session()
    if request.method == 'GET':
        print(id)
        user = session.query(User).get(id)
        schema = UserSchema(many=False)
        user = schema.dump(user)
        session.close()
        return jsonify(user), 200
    if request.method == 'DELETE':
        user = session.query(User).get(id)
        if user == None:
            error = {}
            error['message'] = 'Not Found'
            return jsonify(error), 404
        else:
            session.delete(user)
            session.commit()
            session.close()
            return jsonify({'status ': 'user'+id+'is deleted from postgresql'})




@app.route('/login', methods=['POST'])
def get_user_by_password_username():
    session = Session()
    posted_user = UserSchema(only=('username', 'password')).load(request.get_json())
    print(posted_user['username'])
    user = session.execute(select(User.id,User.username, User.password, User.profil, User.email)\
        .where(User.username == posted_user['username'], User.password == posted_user['password'])).first()
    print(user)
    if user:
        hash = jwt.encode(dict(user),
                    app.config['SECRET_KEY'],
                    algorithm='HS256'
                )
        new_user_json = {}
        new_user_json['token'] = str(hash)
        return jsonify(dict(new_user_json)), 201
    else:
        error = {}
        error['message'] = "user not found!"
        return jsonify(error), 404


@app.route('/host', methods=['GET', 'POST','PUT'])
def get_post_put_host():
    session = Session()
    if request.method == 'GET':
        host_objects = session.query(Host).all()
        schema = HostSchema(many=True)
        host = schema.dump(host_objects)
        session.close()
        return jsonify(host)
    if request.method == 'POST':
        posted_host = HostSchema(only=('name','username', 'password',\
            'ipAddress', 'deploymentPath','nodeElastic' , 'nodeDeploy','description'))\
            .load(request.get_json())
        print(posted_host['name'])
        host = Host("HTTP post request", posted_host)
        session = Session()
        session.add(host)
        session.commit()
        session.close()
        feedbasck = {}
        feedbasck['message'] = 'Request sucess'
        return jsonify(feedbasck), 201
    if request.method == 'PUT':
        body = HostSchema(only=('id','name','username', 'password',\
            'ipAddress', 'deploymentPath','nodeElastic' , 'nodeDeploy','description'))\
            .load(request.get_json())
        host = session.execute(select(Host).where(Host.id == body['id'])).first()
        if host == None:
            error = {}
            error['message'] = 'User Not Found'
            return jsonify(error), 201
        print(body)
        session.execute(update(Host).where(Host.id==body['id']).values(name=body['name'],username=body['username'],\
            password=body['password'], ipAddress=body['ipAddress'],\
            deploymentPath=body['deploymentPath'], nodeElastic=body['nodeElastic'],\
            nodeDeploy=body['nodeDeploy'], description=body['description']))
        session.commit()
        session.close()
        feedback = {}
        feedback['message'] = 'statu host'+str(body['id'])+'is updated from postgresql'
        return jsonify(feedback), 201



@app.route('/host/<id>', methods=['GET', 'DELETE'])
def edit_get_remove_host_by_id(id):
    session = Session()
    if request.method == 'GET':
        print(id)
        host = session.query(Host).get(id)
        if host == None:
            error = {}
            error['message'] = 'Not Found'
            return jsonify(error), 404
        schema = HostSchema(many=False)
        host = schema.dump(host)
        session.close()
        return jsonify(host), 200
    if request.method == 'DELETE':
        host = session.query(Host).get(id)
        if host == None:
            error = {}
            error['message'] = 'Not Found'
            return jsonify(error), 404
        else:
            session.delete(host)
            session.commit()
            session.close()
            return jsonify({'status ': 'host'+id+'is deleted from postgresql'})


@app.route('/script', methods=['GET', 'POST','PUT'])
def get_post_put_script():
    session = Session()
    if request.method == 'GET':
        host_objects = session.query(Script).all()
        schema = ScriptSchema(many=True)
        script = schema.dump(host_objects)
        session.close()
        return jsonify(script)
    if request.method == 'POST':
        posted_script = ScriptSchema(only=('name','domaine',\
        'fileType', 'location','collectScript', 'parsingScript', 'configFiles', 'description'))\
            .load(request.get_json())
        print(posted_script['name'])
        script = Script("HTTP post request", posted_script)
        session = Session()
        session.add(script)
        session.commit()
        session.close()
        feedbasck = {}
        feedbasck['message'] = 'Request sucess'
        return jsonify(feedbasck), 201
    if request.method == 'PUT':
        body = ScriptSchema(only=('id','name','domaine', 'fileType',\
            'location', 'collectScript','parsingScript' , 'configFiles','description'))\
            .load(request.get_json())
        script = session.execute(select(Script).where(Script.id == body['id'])).first()
        if script == None:
            error = {}
            error['message'] = 'User Not Found'
            return jsonify(error), 201
        print(body)
        session.execute(update(Script).where(Script.id==body['id']).values(name=body['name'],\
            domaine=body['domaine'], fileType=body['fileType'],\
            location=body['location'], collectScript=body['collectScript'],\
            parsingScript=body['parsingScript'], description=body['description']))
        session.commit()
        session.close()
        feedback = {}
        feedback['message'] = 'statu script'+str(body['id'])+'is updated from postgresql'
        return jsonify(feedback), 201


@app.route('/script/<id>', methods=['GET', 'DELETE'])
def edit_get_remove_script_by_id(id):
    session = Session()
    if request.method == 'GET':
        print(id)
        script = session.query(Script).get(id)
        if script == None:
            error = {}
            error['message'] = 'Not Found'
            return jsonify(error), 404
        schema = ScriptSchema(many=False)
        script = schema.dump(script)
        session.close()
        return jsonify(script), 200
    if request.method == 'DELETE':
        script = session.query(Script).get(id)
        if script == None:
            error = {}
            error['message'] = 'Not Found'
            return jsonify(error), 404
        else:
            session.delete(script)
            session.commit()
            session.close()
            return jsonify({'status ': 'script'+id+'is deleted from postgresql'})



@app.route('/sourceps/<name>', methods=['GET', 'POST'])
def get_post_put_otarie(name):
    session = Session()
    print(name)
    if request.method == 'GET' and name == 'otarie':
        source_objects = session.query(Otarie).all()
        schema = OtarieSchema(many=True)
        sources = schema.dump(source_objects)
        session.close()
        return jsonify(sources)
    if request.method == 'POST' and name == 'otarie':
        posted_source = OtarieSchema(only=('name','path','accessMode','username',\
              'password', 'ipAddress', 'hostName', 'scriptAssociate','fileType', 'pattern', \
              'date', 'format', 'separateur', 'dateField',\
              'indexName','domaine', 'description'))\
            .load(request.get_json())
        print(posted_source)
        print("----------------")
        script = session.execute( 
             select(Script.name).where(Script.name == posted_source['scriptAssociate'])).first()
        if script == None:
            error = {}
            error['message'] = "Le scripts associer n'existe pas!"
            return jsonify(error), 304
        
        host_info = dict(session.execute(select(Host.username, Host.password, Host.ipAddress, Host.deploymentPath)\
            .where(Host.name == posted_source['hostName'])).first())
        elstict_info = session.execute(select(Host.ipAddress).where(Host.nodeElastic == 'oui')).all()
        all_host = []
        for ip in elstict_info:
            all_host.append("".join(ip))
        all_host = ",".join(all_host)
        print(all_host)
        new_src = source.ConfigFileOtarie(dict(posted_source),host_info, all_host)
        new_src.update_collecte_config_file()
        new_src.update_parsing_config_file()
        new_src.update_elastic_config_file()
        feedback = new_src.create_new_source()
        if type(feedback) == str:
            error = {}
            error['message'] = feedback
            return jsonify(error), 301
        print(feedback)
        sources = Otarie("HTTP post request", posted_source)
        session.add(sources)
        session.commit() 
        
        # return created source
        return jsonify(feedback), 201

    if request.method == 'GET' and name == 'u2020Other':
        source_objects = session.query(U2020Others).all()
        schema = U2020OthersSchema(many=True)
        sources = schema.dump(source_objects)
        session.close()
        return jsonify(sources)
    if request.method == 'POST' and name == 'u2020Other':
        posted_source = U2020OthersSchema(only=('name','path','accessMode','username',\
              'password', 'ipAddress', 'hostName', 'scriptAssociate','fileType', 'pattern', \
              'date', 'format','patternToCopy','patternToNotCopy',\
              'indexName','domaine', 'description'))\
            .load(request.get_json())
        print(posted_source)
        print("----------------")
        script = session.execute( 
             select(Script.name).where(Script.name == posted_source['scriptAssociate'])).first()
        if script == None:
            error = {}
            error['message'] = "Le scripts associer n'existe pas!"
            return jsonify(error), 304
        
        host_info = dict(session.execute(select(Host.username, Host.password, Host.ipAddress, Host.deploymentPath)\
            .where(Host.name == posted_source['hostName'])).first())
        elstict_info = session.execute(select(Host.ipAddress).where(Host.nodeElastic == 'oui')).all()
        all_host = []
        for ip in elstict_info:
            all_host.append("".join(ip))
        all_host = ",".join(all_host)
        print(all_host)
        new_src = source. CreateU2020Others(dict(posted_source),host_info, all_host)
        new_src.update_collecte_config_file()
        new_src.update_parsing_config_file()
        new_src.update_elastic_config_file()
        feedback = new_src.create_new_source()
        if type(feedback) == str:
            error = {}
            error['message'] = feedback
            return jsonify(error), 301
        print(feedback)
        posted_source['pattern'] = ''
        sources = U2020Others("HTTP post request", posted_source)
        session.add(sources)
        session.commit() 
        
        # return created source
        return jsonify(feedback), 201

@app.route('/u2020Other/<id>', methods=['GET', 'DELETE'])
def edit_get_remove_u2020Other_by_id(id):
    session = Session()
    if request.mehod == 'GET':
        print(id)
        u2020Other = session.query(U2020Others).get(id)
        if u2020Other == None:
            error = {}
            error['message'] = 'Not Found'
            return jsonify(error), 404
        schema = U2020OthersSchema(many=False)
        u2020Other = schema.dump(u2020Other)
        session.close()
        return jsonify(u2020Other), 200
    if request.method == 'DELETE':
        u2020Other = session.query(U2020Others).get(id)
        if u2020Other == None:
            error = {}
            error['message'] = 'Not Found'
            return jsonify(error), 404
        else:
            session.delete(u2020Other)
            session.commit()
            session.close()
            return jsonify({'status ': 'u2020Other'+id+'is deleted from postgresql'})

@app.route('/_search/<item>', methods=['POST'])
def search_from_elasticsearch(item):
    if item == 'All':
        posted_search = SearchSchema().load(request.get_json())
        posted_search['index'] = 'otarie-ftpsessions-3h'
        print(posted_search)
        df = elastic.searchall(posted_search)
        print(df)
        if not isinstance(df, pd.DataFrame):
            feedback = {}
            feedback['message'] = df
            return jsonify(feedback), 404
        #dict_df = df.to_dict()
        head = df.head(0)
        print(df.head(10))
        gk = df.groupby('remAS')
        #camb = df[['remAS','servProvider','hostName','app', 'nBytesUp+nBytesDn']]
        print(gk.first())
        #print(gk.get_group('YAHOO-1'))
        #print(gk['nBytesUp+nBytesDn'])
        curve = df[['startTime','delay_SYN_SYNACK','delay_SYNACK_ACK']]
        avg_delay_synack = df['delay_SYN_SYNACK'].astype(float).mean()
        avg_delay_ack = df['delay_SYN_SYNACK'].astype(float).mean()  
        html_df = str(df.to_html())
        html_df = html_df.replace('<table border="1" class="dataframe">', '')
        html_df = html_df.replace('</table>', '')
        #html_df = '<table id="data" style="color: black" class="table table-tripered">'+html_df+'</table>'
        #html_df = BeautifulSoup(html_df)
        feedback = {}
        feedback['table'] = html_df
        for column in curve.columns:
            feedback[list(column.split('_'))[-1]] = curve[column].to_list()
        feedback['avg'] = str(avg_delay_synack)+","+str(avg_delay_ack)
        print(feedback['avg'])
        return jsonify(feedback), 201


    if item == 'One':
        posted_search = SearchSchema().load(request.get_json())
        posted_search['index'] = 'otarie-ftpsessions-3h'
        print(posted_search)
        df = elastic.searchOne(posted_search)
        if df.empty:
            error = {}
            error['message'] = "No data found"
            return jsonify(error), 404
        feedback = {}
        
        dict_df = df.to_dict('index')
        dict_df['header'] = ",".join(list(df.head(0)))
        return jsonify(df.to_html()), 201


"""
@app.route('/host', methods=['GET', 'POST'])
def data_hote():
    if request.method == 'GET':
        session = Session()
        host_objects = session.query(Host).all()
        schema = HostSchema(many=True)
        host = schema.dump(host_objects)
        session.close()
        return jsonify(host)
    if request.method == 'POST':
        posted_host = HostSchema(only=('name','username', 'password',\
            'ipAddress', 'deploymentPath','nodeElastic' , 'nodeDeploy','description'))\
            .load(request.get_json())
        print(posted_host['name'])
        host = Host("HTTP post request", posted_host)
        session = Session()
        session.add(host)
        session.commit()

        # return created source
        new_host = SourceSchema().dump(host)
        session.close()
        return jsonify(new_host), 201

@app.route('/script', methods=['POST', 'GET'])
def data_scripts():
    if request.method == 'GET':
        session = Session()
        script_objects = session.query(Script).all()
        schema = ScriptSchema(many=True)
        scripts = schema.dump(script_objects)
        session.close()
        return jsonify(scripts)

    if request.method == 'POST':
        posted_script = ScriptSchema(only=('name', 'domaine', 'fileType', 'location', 'collectScript', 'parsingScript', 'configFiles', 'description'))\
            .load(request.get_json())
        print(posted_script)
        #new_scp = source.CreateSource(posted_script)
        #new_srp.create_ressource_in_host_deployment()
        #new_srp.associate_script_to_new_source()
        scripts = Script("HTTP post request", posted_script)
        session = Session()
        session.add(scripts)
        session.commit()

        # return created source
        new_script = SourceSchema().dump(scripts)
        session.close()
        return jsonify(new_script), 201

@app.route('/config', methods=['POST', 'GET'])
def data_config():
    if request.method == 'GET':
        session = Session()
        config_objects = session.query(ConfigOtarie1).all()
        schema = ConfigFileOtarie1Schema(many=True)
        configs = schema.dump(config_objects)
        session.close()
        return jsonify(configs)

    if request.method == 'POST':
        posted_script = ConfigFileOtarie1Schema(only=('scriptName', 'date', 'format', 'separateur', 'dateField', 'elasticServer', 'indexName', 'mappingFile'))\
            .load(request.get_json())
        print(posted_script)
        #new_scp = source.CreateSource(posted_script)
        #new_srp.create_ressource_in_host_deployment()
        #new_srp.associate_script_to_new_source()
        configs = ConfigOtarie1("HTTP post request", posted_script)
        session = Session()
        session.add(configs)
        session.commit()

        new_config = ConfigFileOtarie1Schema().dump(configs)
        session.close()
        return jsonify(configs), 201

@app.route('/source/<string:id>', methods=['GET', 'DELETE','PUT'])
def edit_source(id):
    session = Session()
    if request.method == 'GET':
        source_objects = session.query(Source).get(id)
        schema = SourceSchema(many=False)
        host = schema.dump(source_objects)
        session.close()
        return jsonify(host)
    if request.method == 'PUT':
        body = SourceSchema(only=('name','username', 'password', 'ipAddress', 'deploymentStatue', 'deploymentPath', 'nodeElastic'))\
            .load(request.get_json())
        edit_source = session.query(Source).filter_by(id=id).first()
        edit_source.path = body['path']
        edit_source.accessMode = body['accessMode']
        edit_source.username = body['username']
        edit_source.password = body['password']
        edit_source.hostName = body['hostName']
        edit_source.pattern = body['pattern']
        edit_source.domaine = body['domaine']
        edit_source.description = body['description']
        session.commit()
        session.close()
        return jsonify({'status ': 'source'+id+'is updated from postgresql'})
    if request.method == 'DELETE':
        delSource = session.query(Source).filter_by(id=id).first()
        session.delete(delSource)
        session.commit()
        session.close()
        return jsonify({'status ': 'source'+id+'is deleted from postgresql'})
    
def create_source(name, hostname, sourceAssociate):
    #path = os.getcwd()
    session = Session()
    host_info = session.execute(select(Host.username, Host.password, Host.ipAddress ,Host.deploymentPath).where(Host.name == hostname)).first()
    #script_location = session.execute(select(Script.location).where(Script.name == scripname)).first()
    host_info = dict(host_info)
    #print(dict(script_location))
    #script_location = dict(script_location)
    #host_info['name'] = name
    #host_info['script_location'] = scriptlocation
    print(dict(host_info))
    #new_source = source.CreateSource((host_info))
    #info = new_source.create_ressource_in_host_deployment()
    modify_config_file(sourceAssociate , name, host_info)
    #new_source.associate_script_to_new_source()
    session.close()
    return host_info

def modify_config_file(info_source):
        session = Session()
        host_info = session.execute(select(Host.username, Host.password, Host.ipAddress ,Host.deploymentPath).where(Host.name == info_source['hostName'])).first()
    #script_location = session.execute(select(Script.location).where(Script.name == scripname)).first()
        host_info = dict(host_info)

        elastic_host = session.execute(select(Host.ipAddress).where(Host.nodeElastic == 'oui')).first()
        elastic_host = dict(elastic_host)
        print(elastic_host)
        all_host = ",".join(elastic_host.values())
        if info_source['sourceAssociate'] == 'source-otarie':
            elastic_host['hosts'] = all_host
            new_conf = config_file.ConfigFileOtarieS1(info_source,host_info, elastic_host)
            new_conf.update_collecte_config_file()
            new_conf.update_parsing_config_file()
            new_conf.update_elastic_config_file()
            new_conf.create_new_source()
            #new_conf.associate_script_to_new_source(host_info)
        elif info_source['sourceAssociate'] == 'source-scp':
            new_conf = config_file.ConfigFileSCPCDR(info_source, host_info)
            new_conf.update_collecte_config_file()
            new_conf.create_new_source()
        
"""