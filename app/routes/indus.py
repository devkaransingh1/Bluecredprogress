from flask import Blueprint, request, render_template, redirect, url_for, flash, session , jsonify
from app import db
from app.models import Auditor
import random


indus_bp = Blueprint('indus',__name__)


@indus_bp.route('/industries')
def industries():
    if 'auditor' in session:
        return redirect(url_for('auth.industry_records'))
    return render_template('industries.html')


@indus_bp.route("/api/test")
def test_api():

    data = {
        "industry_id": "IND001",
        "co2": random.randint(50, 200),
        "pm25": random.randint(10, 100),
        "water_quality": random.randint(1, 10)
    }

    return jsonify(data)