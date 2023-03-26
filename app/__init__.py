import configparser
import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import urllib.parse


app = Flask(__name__)

location = "config.ini"


def config_parser(location):
    config = configparser.ConfigParser()
    config.read(location)
    host = config['postgresql']['host']
    user = config['postgresql']['user']
    passwd = config['postgresql']['password']
    db = config['postgresql']['db']
    port = config['postgresql']['port']
    return host, user, passwd, db, port


host, user, password, db, port = config_parser(location)
password = urllib.parse.quote(password)
db_uri = f'postgresql://{user}:{password}@{host}:{port}/{db}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app)


from app.sales import database
from app.sales import utils


@app.route('/', methods=['GET'])
def insert_data():
    return database.read_data()


@app.route('/report', methods=['POST'])
def report():
    inp = request.get_json()
    report = utils.generate_report(inp['date'])
    return json.dumps(report)