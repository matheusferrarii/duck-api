from flask import Blueprint, request, jsonify
from app import db
from models import PatoPrimordial, SuperPoder, StatusHibernacao
from schemas import PatoSchema, PoderSchema
from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('patos', __name__)

@bp.route('', methods=['POST'])
def create_pato():
    payload = request.get_json(silent=True)
    current_app.logger.info('POST /patos payload: %s', payload)
    schema = PatoSchema()
    try:
        pato = schema.load(payload)
    except ValidationError as e:
        current_app.logger.warning('ValidationError /patos: %s', e.messages)
        return jsonify({'errors': e.messages}), 400
    except Exception as e:
        current_app.logger.exception('Unexpected error in /patos')
        return jsonify({'error': 'erro interno ao processar payload', 'detail': str(e)}), 500
    db.session.add(pato)
    db.session.commit()
    return jsonify({"id": pato.id}), 201

@bp.route('', methods=['GET'])
def list_patos():
    patos = PatoPrimordial.query.all()
    result = []
    for p in patos:
        result.append({
            'id': p.id,
            'drone_id': p.drone_id,
            'altura_cm': p.altura_cm,
            'peso_g': p.peso_g,
            'cidade': p.cidade,
            'pais': p.pais,
            'lat': p.latitude,
            'lon': p.longitude,
            'precisao_m': p.precisao_m,
            'ponto_referencia': p.ponto_referencia,
            'status': p.status,
            'batimentos_bpm': p.batimentos_bpm,
            'mutacoes': p.mutacoes,
            'poderes': [ {'id': s.id, 'nome': s.nome} for s in p.poderes ]
        })
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def get_pato(id):
    p = PatoPrimordial.query.get_or_404(id)
    return jsonify({
        'id': p.id,
        'drone_id': p.drone_id,
        'altura_cm': p.altura_cm,
        'peso_g': p.peso_g,
        'cidade': p.cidade,
        'pais': p.pais,
        'lat': p.latitude,
        'lon': p.longitude,
        'precisao_m': p.precisao_m,
        'ponto_referencia': p.ponto_referencia,
        'status': p.status,
        'batimentos_bpm': p.batimentos_bpm,
        'mutacoes': p.mutacoes,
        'poderes': [ {'id': s.id, 'nome': s.nome, 'classificacao': s.classificacao} for s in p.poderes ]
    })

@bp.route('/<int:id>', methods=['PUT'])
def update_pato(id):
    p = PatoPrimordial.query.get_or_404(id)
    payload = request.get_json()
    if 'cidade' in payload:
        p.cidade = payload['cidade']
    if 'pais' in payload:
        p.pais = payload['pais']
    if 'mutacoes' in payload:
        p.mutacoes = payload['mutacoes']
    if 'status' in payload:
        p.status = payload['status']
    db.session.commit()
    return jsonify({'message': 'atualizado'})

@bp.route('/<int:id>', methods=['DELETE'])
def delete_pato(id):
    p = PatoPrimordial.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'message': 'removido'})

@bp.route('/<int:id>/poder', methods=['POST'])
def add_poder(id):
    p = PatoPrimordial.query.get_or_404(id)
    if p.status != StatusHibernacao.DESPERTO.value:
        return jsonify({'error': 'poder só pode ser cadastrado se o pato estiver desperto'}), 400
    schema = PoderSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    poder = SuperPoder(nome=data['nome'], descricao=data['descricao'], classificacao=data['classificacao'], pato_id=p.id)
    db.session.add(poder)
    db.session.commit()
    return jsonify({'id': poder.id}), 201
