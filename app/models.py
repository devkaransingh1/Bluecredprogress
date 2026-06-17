from app import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone



# Auditor table
class Auditor(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    blue_id = db.Column(db.String(50), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)

    password = db.Column(db.String(200), nullable=False)

    total_audits = db.Column(db.Integer, default=0)



# Industries table
class Industry(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    industry_id = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    name = db.Column(db.String(150), nullable=False)

    industry_type = db.Column(
        db.String(50)
    )

    location = db.Column(
        db.String(150)
    )

    bluecred_score = db.Column(
        db.Integer
    )

    pollution_status = db.Column(
        db.String(50)
    )

    auditor_id = db.Column(
        db.String(50)
    )

    last_audit_date = db.Column(
        db.Date
    )

    verified = db.Column(
        db.Boolean,
        default=True
    )
    
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )


class IndustryAccess(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    industry_id = db.Column(
        db.String(50),
        db.ForeignKey('industry.industry_id'),
        unique=True,
        nullable=False
    )

    field_verification_key = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )
