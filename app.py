#!flask/bin/python
import os
from flask import Flask, jsonify
from flask import abort, make_response
from flask import request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from models import db, VehicleMake, VehicleModel
from flask import request
from sqlalchemy.orm import sessionmaker, relationship, joinedload

app = Flask(__name__)
CORS(app)

auth = HTTPBasicAuth()

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'. \
    format(user=os.getenv("DB_USER"), pw=os.getenv("DB_PASSWORD"), url=os.getenv("DB_HOST"), db=os.getenv("DB_NAME"))

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


def make_public_vehicle_make(make):
    new_vehicle_make = {}
    for field in make:
        if field == 'id':
            new_vehicle_make['uri'] = url_for('get_vehicle_make', make_id=make['id'], _extenal=True)
    return new_vehicle_make


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/vehicles/api/v1.0/makes/', methods=['GET'])
def fetch_vehicle_makes():
    makes = VehicleMake.query.all()
    return jsonify(makes=[i.serialize for i in makes]), 200


@app.route('/vehicles/api/v1.0/make_models/', methods=['GET'])
def fetch_vehicle_makes_models():
    makes = db.session.query(VehicleMake).options(joinedload(VehicleMake.models)).all()
    return jsonify(Vehicles=[
        dict(c.serialize, models=[i.serialize
                                  for i in c.models])
        for c in makes]), 200


@app.route('/vehicles/api/v1.0/makes/<int:make_id>', methods=['GET'])
def get_vehicle_make(make_id):
    make = VehicleMake.query.filter_by(id=make_id).first()
    return jsonify(make=[make.serialize]), 200


@app.route('/vehicles/api/v1.0/add_vehicle_make', methods=['POST'])
def add_vehicle_make():
    data = request.get_json(force=True)
    vehicle_name = data['name']
    description = data['description']

    add_make = VehicleMake(name=vehicle_name, description=description)
    db.session.add(add_make)
    db.session.commit()
    return jsonify({'response': 'Added new Vehicle'}), 201


@app.route('/vehicles/api/v1.0/add_vehicle_model', methods=['POST'])
def add_vehicle_model():
    data = request.get_json(force=True)
    make_id = data['make_id']
    year = data['year']
    price = data['price']
    vehicle_name = data['name']
    description = data['description']

    add_make = VehicleModel(make_id=make_id, name=vehicle_name, year=year, price=price, description=description)
    db.session.add(add_make)
    db.session.commit()
    return jsonify({'response': 'Added new Vehicle Model'}), 201


@app.route('/vehicles/api/v1.0/get_vehicle_models/<int:make_id>', methods=['GET'])
def get_vehicle_models(make_id):
    models = VehicleModel.query.filter_by(make_id=make_id).all()
    return jsonify(models=[i.serialize for i in models]), 200


if __name__ == '__main__':
    app.run(debug=True)
