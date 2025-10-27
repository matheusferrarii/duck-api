from flask import Blueprint, jsonify
from models import PatoPrimordial, StatusHibernacao

bp = Blueprint('analise', __name__)

@bp.route('/<int:id>', methods=['GET'])
def analise(id):
    p = PatoPrimordial.query.get_or_404(id)
    score_valor = min(100, p.mutacoes * 10)
    score_tamanho = (p.altura_cm / 100.0) * 20 + (p.peso_g / 1000.0) * 10
    risco = 0
    if p.status == StatusHibernacao.DESPERTO.value:
        risco += 50
    elif p.status == StatusHibernacao.TRANSE.value:
        risco += 20
    if p.batimentos_bpm:
        if p.batimentos_bpm > 120:
            risco += 30
        elif p.batimentos_bpm > 80:
            risco += 10
    poder_risco = 0
    for s in p.poderes:
        if 'bélico' in (s.classificacao or '').lower() or 'alto' in (s.classificacao or '').lower():
            poder_risco += 30
        elif 'raro' in (s.classificacao or '').lower():
            poder_risco += 10
    risco += poder_risco
    custo_operacional = score_tamanho * (1 + risco/100.0)
    ganho_conhecimento = score_valor + sum(20 for s in p.poderes if 'raro' in (s.classificacao or '').lower())
    return jsonify({'id': p.id, 'risco_est': round(min(100, risco), 2), 'custo_operacional_est': round(custo_operacional, 2), 'valor_cientifico_est': round(ganho_conhecimento, 2)})
