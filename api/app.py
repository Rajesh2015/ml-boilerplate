import os
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
import requests
# import logging
import json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_ENDPOINT')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/', methods=['GET'])
def root_response():
    """Info."""
    response = make_response("ML-Boilerplate API. Endpoints: /api/v1.0/test, /api/v1.0/predict")
    return response


@app.route('/api/v1.0/fruits', methods=['GET', 'POST'])
def fruits():
    """Handle fruits (Postgres integration)"""
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_fruit = FruitsModel(name=data['name'], price=data['price'])
            db.session.add(new_fruit)
            db.session.commit()
            return {"message": f"fruit {new_fruit.name} has been created successfully."}
        else:
            return make_response({"error": "The request payload is not in JSON format"}, 400)
    elif request.method == 'GET':
        seed()
        fruits = FruitsModel.query.all()
        results = [
            {
                "name": fruit.name,
                "price": fruit.price
            } for fruit in fruits]
        return make_response({"items": results})


@app.route('/api/v1.0/predict', methods=['POST', 'OPTIONS'])
def predict_response():
    """Execute a prediction."""
    try:
        data = json.dumps(request.json)
        headers = {'Content-type': 'application/json'}
        url = os.environ.get('MLFLOW_ENDPOINT')
        post_response = requests.post(url, data=data, headers=headers)
        return make_response(jsonify(post_response.json()))
    except Exception as exc:
        app.logger.error(exc)
        return make_response({'error': 'Error calling model engine: ' + str(exc)}, 500)


def seed():
    fruits = FruitsModel.query.all()
    if len(fruits) == 0:
        db.session.add(FruitsModel(name='Apples', price=1.2))
        db.session.add(FruitsModel(name='Oranges', price=3.4))
        db.session.commit()


class FruitsModel(db.Model):
    __tablename__ = 'fruits'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.String())

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"<Fruit {self.name}>"
