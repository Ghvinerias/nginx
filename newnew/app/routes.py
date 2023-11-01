import os
from flask import request, jsonify
from app import app
from .mongo import MongoAPI

MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_PORT = int(os.environ.get('MONGO_PORT'))
MONGO_DB = os.environ.get('MONGO_DB')
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')

mongo = MongoAPI()
mongo.connect(MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_USER, MONGO_PASS)


@app.route('/test', methods=['GET'])
def test_mongodb_connection():
    return jsonify(mongo.test_connection())

@app.route('/upload_file', methods=['POST'])
def upload_file():
    data = request.get_json()
    file_name = data.get('file_name')
    file_path = data.get('file_path')
    return jsonify(mongo.upload_file(file_name, file_path))

@app.route('/generate_config', methods=['POST'])
def generate_config():
    data = request.get_json()
    return jsonify(mongo.generate_config(data))

@app.route('/list_configs', methods=['GET'])
def list_configs():
    return jsonify(mongo.list_configs())

@app.route('/list_templates', methods=['GET'])
def list_templates():
    return jsonify(mongo.list_templates())

@app.route('/show_template', methods=['POST'])
def show_template():
    data = request.get_json()
    template_name = data.get('template_name')
    return jsonify(mongo.show_template(template_name))

@app.route('/get_config', methods=['POST'])
def get_config():
    data = request.get_json()
    config_name = data.get('config_name')
    return jsonify(mongo.get_config(config_name))
