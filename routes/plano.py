from flask import Blueprint, jsonify
from models import PatoPrimordial, StatusHibernacao

bp = Blueprint('plano', __name__)

@bp.route('/<int:id>', methods=['GET'])
def plano(id):
    p = PatoPrimordial.query.get_or_404(id)
    steps = []
    if p.status == StatusHibernacao.DESPERTO.value:
        steps.append('Montar equipe tática: pato desperto exige contencao e proteções anti-poder.')
    elif p.status == StatusHibernacao.TRANSE.value:
        steps.append('Equipe de contenção + equipe médica: monitorar batimentos e evitar estresse.')
    else:
        steps.append('Equipe de captura leve: hibernação profunda reduz riscos diretos.')
    if p.altura_cm > 100:
        steps.append('Ataque superior: para alvos >100cm, ataque por cima e imobilize peso.')
    if any('fogo' in (s.descricao or '').lower() for s in p.poderes):
        steps.append('Equipar extintores térmicos e escudos anti-rafaga.')
    steps.append('Gerador de Defesas Aleatórias: distração com doce local (ex.: brigadeiros) se sensível a alimentos.)')
    transporte = 'Veículo leve' if p.peso_g < 50000 else 'Transporte pesado (helicóptero/guindaste)'
    return jsonify({'id': p.id, 'steps': steps, 'transporte_sugerido': transporte})

@bp.route('/status_drone', methods=['GET'])
def status_drone():
    status = {
        'bateria': '78%',
        'combustivel': '64%',
        'integridade_fisica': '92%'
    }
    return jsonify(status)

@bp.route('/defesa_aleatoria', methods=['GET'])
def defesa_aleatoria():
    import random
    options = [
        {'defesa': 'Teletransportar crianças para atirar brigadeiros'},
        {'defesa': 'Lançar ursinhos perfumados para confundir o pato'},
        {'defesa': 'Liberar fumaça colorida para distração'},
        {'defesa': 'Ativar escudos eletromagnéticos temporários'}
    ]
    return jsonify(random.choice(options))
