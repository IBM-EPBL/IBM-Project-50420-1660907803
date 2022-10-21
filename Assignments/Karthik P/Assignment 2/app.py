import flask 
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

users_dict = [{'id':1,'name': 'Karthik','age':21},{'id':2,'name':'Aswin Kumar','age':21},{'id':3,'name':'Jasper','age':21},{'id':4,'name':'Nnadakumar','age':21}]
user_dict =[]
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users_dict)

@app.route('/user', methods=['POST'])
def post_users():
    user=request.get_json()
    user['id']=len(user_dict)+1 
    user_dict.append(user)
    return jsonify(user) 

@app.route('/user', methods=['PUT'])
def put_users():
    user=request.get_json()
    for i,u in enumerate(user_dict):
        if u['id'] == user['id']:
            user_dict[i]=user
    return {}

@app.route('/user/<id>', methods=['DELETE'])
def delete_users(id):
    for user in user_dict:
        if user['id'] == int(id):
            user_dict.remove(user)
    return {}

app.run()