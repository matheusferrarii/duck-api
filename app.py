from flask import Flask
from config import Config
from extensions import db
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from models import Drone, PatoPrimordial, SuperPoder
        from services.seed import seed_initial_data
        db.create_all()
        seed_initial_data()

    from routes.drones import bp as drones_bp
    from routes.patos import bp as patos_bp
    from routes.analise import bp as analise_bp
    from routes.plano import bp as plano_bp

    app.register_blueprint(drones_bp, url_prefix='/drones')
    app.register_blueprint(patos_bp, url_prefix='/patos')
    app.register_blueprint(analise_bp, url_prefix='/analise')
    app.register_blueprint(plano_bp, url_prefix='/plano')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
