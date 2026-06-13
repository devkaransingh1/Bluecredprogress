from app import db
from flask_sqlalchemy import SQLAlchemy

class Auditor(db.Model):
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    blue_id = db.Column(db.String(50), unique=True,nullable=False)
    name = db.Column(db.String(100))
    password = db.Column(db.String(200))