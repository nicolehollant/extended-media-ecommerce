import os
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from bson import json_util
from dotenv import load_dotenv
from app.utils import *
from app.client import Client


load_dotenv()
app = Flask(__name__)
CORS(app)


host = os.getenv("DBHOST", "localhost")
port = os.getenv("MONGOPORT", "27017")
username = os.getenv("MONGO_USERNAME", None)
password = os.getenv("MONGO_PASSWORD", None)
admin_username = os.getenv("ADMIN_USERNAME", "admin_username")
admin_password = os.getenv("ADMIN_PASSWORD", "admin_password")

uri = f"mongodb://{host}:{port}"
if username and password:
  uri = f"mongodb://{username}:{password}@{host}:{port}"
dbname = "extendedmedia"

client = Client(uri=uri, dbname=dbname)

print(client.uri, client.dbname)

client.add_collection("users")
client.add_collection("items")
client.add_collection("orders")

# Client.test_ops(client)

routes = Blueprint('routes', __name__)