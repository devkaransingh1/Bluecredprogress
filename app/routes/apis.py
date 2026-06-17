from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from app import db
from app.models import Industry, Auditor , IndustryAccess


apis_bp = Blueprint('apis',__name__)



# industry api - fetches industries data for all industries dashboard for displaying

@apis_bp.route('/api/fetch_industries')
def fetch_industries():
    industries = Industry.query.all()
    data = []
    for industry in industries:
        data.append({
            "industry_id": industry.industry_id,
            "name": industry.name,
            "industry_type": industry.industry_type,
            "location": industry.location,
            "bluecred_score": industry.bluecred_score,
            "pollution_status": industry.pollution_status,
            "auditor_id": industry.auditor_id,
            "last_audit_date": str(industry.last_audit_date),
            "verified": industry.verified
        })
    return jsonify(data)




# auditor dashboard - fetches auditor details from Auditor table to display data.

@apis_bp.route('/api/auditor/me')
def fetch_auditor():
    if 'auditor' not in session:
        return jsonify({"error":"Unauthorized"}),401
    auditor = Auditor.query.filter_by(id=session['auditor']).first()

    if not auditor:
        return jsonify({"error":"Auditor not found"}),404

    return jsonify({
        "id": auditor.blue_id,
        "name": auditor.name,
        "total_audits": auditor.total_audits
    }) 



@apis_bp.route('/api/audit/access', methods=['POST'])
def audit_access():

    data = request.json

    industry_id = data["industry_id"]
    key = data["field_verification_key"]

    access = IndustryAccess.query.filter_by(
        industry_id=industry_id,
        field_verification_key=key
    ).first()

    if not access:
        return jsonify({
            "success": False,
            "error": "Invalid credentials"
        }), 401

    industry = Industry.query.filter_by(
        industry_id=industry_id
    ).first()


    session['loggedin_industry'] = industry_id

    return jsonify({
        "success": True,
        "redirect_url": "/audit_report",
        "industry": {
            "industry_id": industry.industry_id,
            "name": industry.name,
            "type": industry.industry_type,
            "location": industry.location,
            "score": industry.bluecred_score,
            "pollution": industry.pollution_status,
            "auditor": industry.auditor_id
        }
    })


@apis_bp.route('/api/industry/current', methods=['GET'])
def current_industry():

    industry_id = session.get('loggedin_industry')
    auditor_db_id = session.get('auditor')

    if not industry_id:
        return jsonify({"error": "No industry selected"}), 401

    industry = Industry.query.filter_by(industry_id=industry_id).first()
    auditor = Auditor.query.get(auditor_db_id)

    return jsonify({
        "industry_id": industry.industry_id,
        "name": industry.name,
        "type": industry.industry_type,
        "location": industry.location,
        "auditor": auditor.blue_id
    })