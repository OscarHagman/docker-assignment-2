from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from flask import render_template, make_response

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]


class Register(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data["username"]
        password = posted_data["password"]

        users.insert({
            "Username": username,
            "Password": password,
            "Sentence": "",
            "Tokens": 6
        })

        return_json = {
            "status": 200,
            "msg": "You successfully signed up for the API",
            "tokens": 6
        }
        return jsonify(return_json)


def verify_password(username, password):
    user_pw = users.find({
        "Username": username
    })[0]["Password"]

    if user_pw == password:
        return True
    else:
        return False


def count_tokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]

    return tokens


class Store(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data["username"]
        password = posted_data["password"]
        sentence = posted_data["sentence"]

        correct_pw = verify_password(username, password)

        if not correct_pw:
            return_json = {
                "status": 302,
                "msg": "wrong username or password"
            }
            return jsonify(return_json)
        num_tokens = count_tokens(username)
        if num_tokens <= 0:
            return_json = {
                "status": 301,
                "msg": "out of tokens"
            }
            return jsonify(return_json)

        users.update({
            "Username": username
        }, {
            "$set": {
                "Sentence": sentence,
                "Tokens": num_tokens - 1
            }
        })

        return_json = {
            "status": 200,
            "msg": "Sentence saved successfully",
            "tokens": count_tokens(username)
        }
        return jsonify(return_json)


class Get(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data["username"]
        password = posted_data["password"]

        correct_pw = verify_password(username, password)
        if not correct_pw:
            return_json = {
                "status": 302,
                "msg": "wrong username or password"
            }
            return jsonify(return_json)

        num_tokens = count_tokens(username)
        if num_tokens <= 0:
            return_json = {
                "status": 301,
                "msg": "out of tokens"
            }
            return jsonify(return_json)

        users.update({
            "Username": username
        }, {
            "$set": {
                "Tokens": num_tokens-1
            }
        })

        sentence = users.find({
            "Username": username
        })[0]["Sentence"]

        return_json = {
            "status": 200,
            "sentence": str(sentence),
            "tokens": count_tokens(username)
        }

        return jsonify(return_json)


class Index(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)


api.add_resource(Register, "/register")
api.add_resource(Store, "/store")
api.add_resource(Get, "/get")
api.add_resource(Index, "/")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
