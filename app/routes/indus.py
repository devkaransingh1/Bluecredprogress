from flask import Blueprint, request, render_template, redirect, url_for, flash, session , jsonify
from app import db


indus_bp = Blueprint('indus',__name__)


@indus_bp.route('/industries')
def industries():
    if 'auditor' in session:
        return redirect(url_for('auth.auditor_dashboard'))
    return render_template('industries.html')


@indus_bp.route('/industry/reports/<industry_id>')
def industry_reports(industry_id):

    return render_template(
        "industry_reports.html",
        industry_id=industry_id
    )

@indus_bp.route('/industry_registeration')
def industry_registeration():
    if 'auditor' not in session:
        return redirect(url_for('auth.login'))
    return render_template('industry_register.html')


@indus_bp.route('/industry/report/<industry_id>/<report_id>')
def report_details(industry_id, report_id):

    if 'auditor' in session:
        return redirect(url_for('auth.auditor_dashboard'))

    return render_template(
        "report_details.html",
        industry_id=industry_id,
        report_id=report_id
    )