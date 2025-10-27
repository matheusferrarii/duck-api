from datetime import datetime
from enum import Enum
from extensions import db

class Drone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String, unique=True, nullable=False)
    marca = db.Column(db.String)
    fabricante = db.Column(db.String)
    pais_origem = db.Column(db.String)

class SuperPoder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    descricao = db.Column(db.String)
    classificacao = db.Column(db.String)
    pato_id = db.Column(db.Integer, db.ForeignKey('pato_primordial.id'))

class PatoPrimordial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drone_id = db.Column(db.Integer, db.ForeignKey('drone.id'))
    altura_cm = db.Column(db.Float)
    peso_g = db.Column(db.Float)
    cidade = db.Column(db.String)
    pais = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    precisao_m = db.Column(db.Float)
    ponto_referencia = db.Column(db.String)
    status = db.Column(db.String)
    batimentos_bpm = db.Column(db.Integer, nullable=True)
    mutacoes = db.Column(db.Integer, default=0)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    poderes = db.relationship('SuperPoder', backref='pato', cascade='all, delete-orphan')

class StatusHibernacao(Enum):
    DESPERTO = 'desperto'
    TRANSE = 'transe'
    HIBERNACAO_PROFUNDA = 'hibernacao_profunda'
