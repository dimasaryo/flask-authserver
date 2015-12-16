from flask import Flask, jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

app.config['MONGO_HOST'] = 'ds029595.mongolab.com'
app.config['MONGO_PORT'] = 29595
app.config['MONGO_DBNAME'] = 'sinau'
app.config['MONGO_USERNAME'] = 'sinaudb'
app.config['MONGO_PASSWORD'] = 'sinaudb'
mongo = PyMongo(app, config_prefix='MONGO')


class User(object):
    def __init__(self, id, username, password):
        self.id = id
	self.username = username
	self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz')
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

jwt = JWT(app, authenticate, identity)

@app.route('/')
def hello_world():
    message = {
        'test': 'hello world'		    
    }

    resp = jsonify(message)
    resp.status_code = 200

    return resp

@app.route('/login', methods=['POST'])
def login():
    content = request.json

    print content

    resp = jsonify(content)
    resp.status_code = 200

    return resp

if __name__ == '__main__':
    app.run()
