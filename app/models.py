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




class AuditReport(db.Model):

    __tablename__ = "audit_report"
    
    id = db.Column(db.Integer, primary_key=True)

    industry_id = db.Column(db.String(50), nullable=False)
    auditor_id = db.Column(db.String(50), nullable=False)

    pm25 = db.Column(db.Numeric, default=0)
    pm10 = db.Column(db.Numeric, default=0)
    so2 = db.Column(db.Numeric, default=0)
    nox = db.Column(db.Numeric, default=0)
    co = db.Column(db.Numeric, default=0)

    ph = db.Column(db.Numeric, default=7)
    bod = db.Column(db.Numeric, default=0)
    cod = db.Column(db.Numeric, default=0)
    tds = db.Column(db.Numeric, default=0)

    chemical_waste_present = db.Column(db.Boolean, default=False)
    hazardous_waste = db.Column(db.Boolean, default=False)

    treatment_facility = db.Column(db.String(50))
    disposal_method = db.Column(db.Text)

    observations = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    audit_decision = db.Column(db.String(30))
    auditor_remarks = db.Column(db.Text)

    submitted_at = db.Column(db.DateTime, server_default=db.func.now())
    report_hash = db.Column(db.Text, unique=True)