from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'my_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Bluecred.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.indus import indus_bp
    from app.routes.apis import apis_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(indus_bp)
    app.register_blueprint(apis_bp)


    return app
