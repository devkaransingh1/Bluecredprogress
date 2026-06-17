from flask import Blueprint, request, render_template, redirect, url_for, flash, session , jsonify
from app import db


indus_bp = Blueprint('indus',__name__)


@indus_bp.route('/industries')
def industries():
    if 'auditor' in session:
        return redirect(url_for('auth.industry_records'))
    return render_template('industries.html')

