import os
import pymongo
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# MongoDB Connection
def get_mongo_connection():
    try:
        # Access environment variables for MongoDB connection
        username = os.environ.get('MONGODB_USERNAME')
        password = os.environ.get('MONGODB_PASSWORD')
        host = os.environ.get('MONGODB_HOST')
        port = os.environ.get('MONGODB_PORT')
        database_name = os.environ.get('MONGODB_DATABASE_NAME')

        client = pymongo.MongoClient(f"mongodb://{username}:{password}@{host}:{port}/{database_name}")
        db = client[database_name]
        return db
    except Exception as e:
        print(f"Connection failed. Error: {e}")
        return None

# Function for testing MongoDB connection
@app.route('/test_mongodb_connection', methods=['GET'])
def test_mongodb_connection():
    try:
        collection_name = request.args.get('collection')
        db = get_mongo_connection()
        if db:
            collection_names = db.list_collection_names()
            return jsonify({'status': 'success', 'message': 'MongoDB connection successful', 'collections': collection_names})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to connect to MongoDB'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Function for uploading a file to MongoDB
@app.route('/upload_file', methods=['POST'])
def upload_file():
    try:
        data = request.get_json()
        filename = data.get("filename")
        file_data = data.get("data")
        collection_name = data.get("collection")  # Adjust as necessary

        db = get_mongo_connection()
        if db:
            collection = db[collection_name]
            file_data = {
                "filename": filename,
                "data": file_data
            }
            collection.insert_one(file_data)
            return jsonify({'status': 'success', 'message': 'File uploaded successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to connect to MongoDB'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Function for retrieving a file from MongoDB based on the provided name and collection
@app.route('/retrieve_config', methods=['POST'])
def retrieve_config():
    try:
        data = request.get_json()
        name = data.get("name")
        collection_name = data.get("collection")  # Adjust as necessary

        db = get_mongo_connection()
        if db:
            collection = db[collection_name]
            file_data = collection.find_one({"filename": name})
            if file_data:
                return jsonify(file_data)
            else:
                return jsonify({'status': 'error', 'message': 'File not found'}), 404
        else:
            return jsonify({'status': 'error', 'message': 'Failed to connect to MongoDB'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Function for generating a new file and saving it to MongoDB
@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        template_filename = data.get("template_filename")
        application_dns = data.get("application_dns")
        application_port = data.get("application_port")
        application_name = data.get("application_name")
        ssl_cert_cer = data.get("ssl_cert_cer")
        ssl_cert_key = data.get("ssl_cert_key")
        collection_name = data.get("collection")  # Adjust as necessary
        name = data.get("name")

        db = get_mongo_connection()
        if db:
            collection = db[collection_name]
            # Perform string replacement to generate the content
            content = "Example generated content based on the provided parameters."
            # Insert the generated file into the MongoDB collection
            file_data = {
                "filename": f"{name}.config",
                "data": content
            }
            collection.insert_one(file_data)
            return jsonify({'status': 'success', 'message': 'File generated and saved successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to connect to MongoDB'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
