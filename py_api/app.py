import os
import pymongo
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set up the MongoDB connection string
username = os.environ.get("username")
password = os.environ.get("password")
host = os.environ.get("host")
port = os.environ.get("port")
auth_db = os.environ.get("auth_db")
data_db = os.environ.get("data_db")
collection_name = os.environ.get("collection_name")

# Establish a connection to MongoDB
try:
    auth_client = pymongo.MongoClient(f"mongodb://{username}:{password}@{host}:{port}/{auth_db}")
    data_client = pymongo.MongoClient(f"mongodb://{username}:{password}@{host}:{port}/{data_db}")
    auth_db = auth_client[auth_db]
    data_db = data_client[data_db]
    collection = data_db["your_collection_name"]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/modify_conf', methods=['POST'])
def modify_conf():
    data = request.get_json()
    application_dns = data.get("application_dns")
    application_port = data.get("application_port")
    application_name = data.get("application_name")
    ssl_cert_cer = data.get("ssl_cert_cer")
    ssl_cert_key = data.get("ssl_cert_key")

    try:
        conf_data = collection.find_one({"filename": "Nginx_Default.conf"})
        if conf_data:
            conf_content = conf_data["data"].decode('utf-8')  # Assuming the data is stored as binary
            conf_content = conf_content.replace("application_dns", application_dns)
            conf_content = conf_content.replace("application_port", application_port)
            conf_content = conf_content.replace("application_name", application_name)
            conf_content = conf_content.replace("ssl_cert_cer", ssl_cert_cer)
            conf_content = conf_content.replace("ssl_cert_key", ssl_cert_key)

            folder_name = f"{application_name}.conf"
            with open(folder_name, 'w') as file:
                file.write(conf_content)
            return jsonify({
                "status": True,
                "error": None,
                "data": conf_content
            })
        else:
            return jsonify({
                "status": False,
                "error": "File not found",
                "data": None
            })
    except Exception as e:
        return jsonify({
            "status": False,
            "error": f"An error occurred: {e}",
            "data": None
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

#test