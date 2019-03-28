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

DB_URL = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
    user=os.getenv("DB_USER"),
    pw=os.getenv("DB_PASSWORD"),
    url=os.getenv("DB_HOST"),
    db=os.getenv("DB_NAME"),
)

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def make_public_vehicle_make(make):
    new_vehicle_make = {}
    for field in make:
        if field == "id":
            new_vehicle_make["uri"] = url_for(
                "get_vehicle_make", make_id=make["id"], _extenal=True
            )
    return new_vehicle_make


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


# Service to get all vehicle makes
@app.route("/vehicles/api/v1.0/makes/", methods=["GET"])
def fetch_vehicle_makes():
    makes = VehicleMake.query.all()
    return jsonify(makes=[i.serialize for i in makes]), 200


# A service to get all vehicle makes with their models
@app.route("/vehicles/api/v1.0/make_models/", methods=["GET"])
def fetch_vehicle_makes_models():
    makes = db.session.query(VehicleMake).options(joinedload(VehicleMake.models)).all()
    return (
        jsonify(
            Vehicles=[
                dict(c.serialize, models=[i.serialize for i in c.models]) for c in makes
            ]
        ),
        200,
    )


# Service to get all vehicle models
@app.route("/vehicles/api/v1.0/get_vehicle_models/<int:make_id>", methods=["GET"])
def get_vehicle_models(make_id):
    models = VehicleModel.query.filter_by(make_id=make_id).all()
    return jsonify(models=[i.serialize for i in models]), 200


# Service to get a specific vehicle make
@app.route("/vehicles/api/v1.0/makes/<int:make_id>", methods=["GET"])
def get_vehicle_make(make_id):
    make = VehicleMake.query.filter_by(id=make_id).first()
    return jsonify(make=[make.serialize]), 200


# Service to add a vehicle make
@app.route("/vehicles/api/v1.0/add_vehicle_make", methods=["POST"])
def add_vehicle_make():
    data = request.get_json(force=True)
    vehicle_name = data["name"]
    description = data["description"]

    add_make = VehicleMake(name=vehicle_name, description=description)
    db.session.add(add_make)
    db.session.commit()
    return jsonify({"response": "Added new Vehicle"}), 201


# Service to add a vehicle model
@app.route("/vehicles/api/v1.0/add_vehicle_model", methods=["POST"])
def add_vehicle_model():
    data = request.get_json(force=True)
    make_id = data["make_id"]
    year = data["year"]
    price = data["price"]
    vehicle_name = data["name"]
    description = data["description"]

    add_make = VehicleModel(
        make_id=make_id,
        name=vehicle_name,
        year=year,
        price=price,
        description=description,
    )
    db.session.add(add_make)
    db.session.commit()
    return jsonify({"response": "Added new Vehicle Model"}), 201


# Service to edit a vehicle make
@app.route("/vehicles/api/v1.0/update_vehicle_make/<int:make_id>", methods=["PUT"])
def update_vehicle_make(make_id):
    data = request.get_json(force=True)
    make = VehicleMake.query.filter_by(id=make_id).first()
    if data["name"]:
        make.name = data["name"]
    if data["description"]:
        make.description = data["description"]
    db.session.commit()
    return jsonify({"response": "Vehicle make updated successfully"}), 201


# Service to edit a vehicle model
@app.route("/vehicles/api/v1.0/update_vehicle_model/<int:model_id>", methods=["PUT"])
def update_vehicle_make_model(model_id):
    data = request.get_json(force=True)
    make_id = data["make_id"]
    year = data["year"]
    price = data["price"]
    vehicle_model = VehicleModel.query.filter_by(id=model_id).first()
    if make_id:
        vehicle_model.make_id = make_id
    if year:
        vehicle_model.year = year
    if price:
        vehicle_model.price = price
    if data["name"]:
        vehicle_model.name = data["name"]
    if data["description"]:
        vehicle_model.description = data["description"]
    db.session.commit()
    return jsonify({"response": "Vehicle model updated successfully"}), 201


# Service to delete a vehicle make
@app.route("/vehicles/api/v1.0/delete_make/<int:make_id>", methods=["DELETE"])
def delete_vehicle_make(make_id):
    VehicleMake.query.filter_by(id=make_id).delete()
    db.session.commit()
    return jsonify({"response": "Deleted a Vehicle make"}), 201


# Service to delete a vehicle model
@app.route("/vehicles/api/v1.0/delete_model/<int:model_id>", methods=["DELETE"])
def delete_vehicle_model(model_id):
    VehicleModel.query.filter_by(id=model_id).delete()
    db.session.commit()
    return jsonify({"response": "Deleted a Vehicle model"}), 201


if __name__ == "__main__":
    app.run(debug=True)
