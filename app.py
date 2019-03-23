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

tasks = [
    {
        'id': 1,
        'title': u'Macedes Benz',
        'description': u'A nice long lasting car, maintenance though',
        'done': False
    },
    {
        'id': 2,
        'title': u'Volkswagan VW',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    },
    {
        'id': 3,
        'title': u'Toyota Land cruiser',
        'description': u'Need to find a good way of handling assignments',
        'done': False
    }
]


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@app.route('/vehicles/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route('/vehicles/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})


@app.route('/vehicles/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': make_public_task(task[0])})


@app.route('/vehicles/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


@app.route('/vehicles/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


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
