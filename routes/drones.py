from flask import Blueprint, request, jsonify
from app import db
from models import Drone
from schemas import DroneSchema

bp = Blueprint('drones', __name__)

@bp.route('', methods=['POST'])
def create_drone():
    schema = DroneSchema()
    data = request.get_json()
    try:
        drone = schema.load(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    db.session.add(drone)
    db.session.commit()
    return schema.dump(drone), 201

@bp.route('', methods=['GET'])
def list_drones():
    schema = DroneSchema(many=True)
    drones = Drone.query.all()
    return jsonify(schema.dump(drones))
