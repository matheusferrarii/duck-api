from marshmallow import Schema, fields, post_load, ValidationError, validates, validates_schema
from models import PatoPrimordial, Drone, StatusHibernacao
from utils import feet_to_cm, lbs_to_g, yards_to_m

class DroneSchema(Schema):
    id = fields.Int(dump_only=True)
    serial = fields.Str(required=True)
    marca = fields.Str()
    fabricante = fields.Str()
    pais_origem = fields.Str()

    @post_load
    def make_drone(self, data, **kwargs):
        return Drone(**data)

class PatoSchema(Schema):
    id = fields.Int(dump_only=True)
    drone_id = fields.Int(required=True)
    altura = fields.Dict(required=True)
    peso = fields.Dict(required=True)
    cidade = fields.Str(required=True)
    pais = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    precisao = fields.Dict(required=True)
    ponto_referencia = fields.Str(allow_none=True)
    status = fields.Str(required=True)
    batimentos = fields.Int(allow_none=True)
    mutacoes = fields.Int(required=True)

    @validates('status')
    def validate_status(self, value):
        if value not in [s.value for s in StatusHibernacao]:
            raise ValidationError('status inválido')

    @validates_schema
    def validate_batimentos(self, data, **kwargs):
        st = data.get('status')
        b = data.get('batimentos')
        if st in (StatusHibernacao.TRANSE.value, StatusHibernacao.HIBERNACAO_PROFUNDA.value) and b is None:
            raise ValidationError('batimentos obrigatórios para transe ou hibernação profunda')

    def _convert_altura(self, altura):
        if not isinstance(altura, dict):
            raise ValidationError('altura deve ser um objeto com value e unit')
        v = altura.get('value')
        if v is None:
            raise ValidationError('altura.value é obrigatório')
        try:
            v = float(v)
        except (TypeError, ValueError):
            raise ValidationError('altura.value deve ser numérico')
        u = altura.get('unit', '').lower()
        if u in ['cm', 'centimeter', 'centimetro', 'centimetros']:
            return v
        if u in ['m', 'meter', 'metros']:
            return v * 100.0
        if u in ['ft', 'feet', 'pé', 'pes']:
            return feet_to_cm(v)
        raise ValidationError('unidade de altura não suportada')

    def _convert_peso(self, peso):
        if not isinstance(peso, dict):
            raise ValidationError('peso deve ser um objeto com value e unit')
        v = peso.get('value')
        if v is None:
            raise ValidationError('peso.value é obrigatório')
        try:
            v = float(v)
        except (TypeError, ValueError):
            raise ValidationError('peso.value deve ser numérico')
        u = peso.get('unit', '').lower()
        if u in ['g', 'gram', 'grama', 'gramas']:
            return v
        if u in ['kg', 'kilogram', 'quilograma', 'kilogramas']:
            return v * 1000.0
        if u in ['lb', 'lbs', 'pound', 'libra', 'libras']:
            return lbs_to_g(v)
        raise ValidationError('unidade de peso não suportada')

    def _convert_precisao(self, precisao):
        if not isinstance(precisao, dict):
            raise ValidationError('precisao deve ser um objeto com value e unit')
        v = precisao.get('value')
        if v is None:
            raise ValidationError('precisao.value é obrigatório')
        try:
            v = float(v)
        except (TypeError, ValueError):
            raise ValidationError('precisao.value deve ser numérico')
        u = precisao.get('unit', '').lower()
        if u in ['m', 'meter', 'metros']:
            return v
        if u in ['cm', 'centimetro', 'centimetros']:
            return v / 100.0
        if u in ['yd', 'yard', 'yards', 'jarda', 'yardas']:
            return yards_to_m(v)
        raise ValidationError('unidade de precisao não suportada')
    
    @post_load
    def make_pato(self, data, **kwargs):
        altura_cm = self._convert_altura(data.pop('altura'))
        peso_g = self._convert_peso(data.pop('peso'))
        precisao_m = self._convert_precisao(data.pop('precisao'))
        batimentos = data.pop('batimentos', None)
        pato = PatoPrimordial(
            drone_id=data['drone_id'],
            altura_cm=altura_cm,
            peso_g=peso_g,
            cidade=data['cidade'],
            pais=data['pais'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            precisao_m=precisao_m,
            ponto_referencia=data.get('ponto_referencia'),
            status=data['status'],
            batimentos_bpm=batimentos,
            mutacoes=data['mutacoes']
        )
        return pato

class PoderSchema(Schema):
    nome = fields.Str(required=True)
    descricao = fields.Str(required=True)
    classificacao = fields.Str(required=True)

