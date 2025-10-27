from extensions import db
from models import Drone, PatoPrimordial, SuperPoder, StatusHibernacao
from utils import feet_to_cm, lbs_to_g, yards_to_m

def seed_initial_data():
    if Drone.query.first():
        return
    d1 = Drone(serial='DRN-0001', marca='Astra', fabricante='AstraTech', pais_origem='BR')
    d2 = Drone(serial='DRN-0002', marca='Pioneer', fabricante='Pioneer Dynamics', pais_origem='US')
    db.session.add_all([d1, d2])
    db.session.commit()

    p1 = PatoPrimordial(drone_id=d1.id, altura_cm=120.0, peso_g=25000.0, cidade='Marília', pais='BR', latitude=-22.2158, longitude=-49.9456, precisao_m=0.5, ponto_referencia='Estação Central', status=StatusHibernacao.TRANSE.value, batimentos_bpm=75, mutacoes=3)
    p2 = PatoPrimordial(drone_id=d2.id, altura_cm=feet_to_cm(6.5), peso_g=lbs_to_g(220), cidade='Unknown Base', pais='US', latitude=37.7749, longitude=-122.4194, precisao_m=yards_to_m(3), ponto_referencia='Pico da Neblina', status=StatusHibernacao.DESPERTO.value, batimentos_bpm=None, mutacoes=8)
    db.session.add_all([p1, p2])
    db.session.commit()

    poder = SuperPoder(nome='Tempestade Elétrica', descricao='Gera descargas elétricas em área', classificacao='bélico, raro', pato_id=p2.id)
    db.session.add(poder)
    db.session.commit()
