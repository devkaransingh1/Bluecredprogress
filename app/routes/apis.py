from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from app import db
from app.models import Industry, Auditor , IndustryAccess , AuditReport
import hashlib
import json

apis_bp = Blueprint('apis',__name__)



# industry api - fetches industries data for all industries dashboard for displaying

@apis_bp.route('/api/fetch_industries')
def fetch_industries():

    industries = Industry.query.all()
    data = []

    for industry in industries:

        latest_report = (
            AuditReport.query
            .filter_by(industry_id=industry.industry_id)
            .order_by(AuditReport.submitted_at.desc())
            .first()
        )

        data.append({
            "industry_id": industry.industry_id,
            "name": industry.name,
            "industry_type": industry.industry_type,
            "location": industry.location,
            "bluecred_score": industry.bluecred_score,
            "pollution_status": industry.pollution_status,

            # 👇 derived from AuditReport (NOT Industry)
            "auditor_id": latest_report.auditor_id if latest_report else None,
            "last_audit_date": latest_report.submitted_at.date().isoformat() if latest_report else None,

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


def generate_hash(data):
    raw = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()

@apis_bp.route('/api/audit/submit-report', methods=['POST'])
def submit_report():

    data = request.json

    m_air = data["measurements"]["air"]
    m_water = data["measurements"]["water"]
    m_waste = data["measurements"]["waste"]
    assessment = data["assessment"]

    report = AuditReport(
        industry_id=data["industry_id"],
        auditor_id=data["auditor_id"],

        pm25=m_air.get("pm25", 0),
        pm10=m_air.get("pm10", 0),
        so2=m_air.get("so2", 0),
        nox=m_air.get("nox", 0),
        co=m_air.get("co", 0),

        ph=m_water.get("ph", 7),
        bod=m_water.get("bod", 0),
        cod=m_water.get("cod", 0),
        tds=m_water.get("tds", 0),

        chemical_waste_present=(m_water.get("chemical_waste_present") == "Yes"),
        hazardous_waste=(m_waste.get("hazardous_generated") == "Yes"),

        treatment_facility=m_waste.get("treatment_facility"),
        disposal_method=m_waste.get("disposal_method_details"),

        observations=assessment.get("observations"),
        recommendations=assessment.get("recommendations"),
        audit_decision=assessment.get("decision"),
        auditor_remarks=assessment.get("remarks"),

        report_hash=generate_hash(data)
    )

    db.session.add(report)
    db.session.commit()

    # =========================
    # STORE ONLY SUMMARY IN SESSION
    # =========================
    session["audit_result"] = {
        "report_id": f"REP-{report.id:06d}",
        "report_hash": report.report_hash,
        "submitted_at": str(report.submitted_at),
        "industry_id": report.industry_id,
        "auditor_id": report.auditor_id
    }

    return jsonify({
        "success": True,
        "redirect_url": "/thankyou"
    })


@apis_bp.route('/api/audit/summary', methods=['GET'])
def audit_summary():

    data = session.get("audit_result")

    if not data:
        return jsonify({"error": "No audit session found"}), 401

    return jsonify(data)


@apis_bp.route('/api/auth/logout', methods=['POST'])
def logout():

    session.clear()

    return jsonify({
        "success": True,
        "message": "Session cleared"
    })



@apis_bp.route('/api/public/industry/<industry_id>/reports', methods=['GET'])
def get_industry_reports(industry_id):

    reports = AuditReport.query.filter_by(
        industry_id=industry_id
    ).order_by(
        AuditReport.submitted_at.desc()
    ).all()


    if not reports:
        return jsonify({
            "success": False,
            "message": "No audit reports found"
        }),404



    data=[]


    for report in reports:

        data.append({

            "report_id":
            f"REP-{report.id:06d}",


            "industry_id":
            report.industry_id,


            "audit_date":
            report.submitted_at.strftime("%d-%m-%Y"),


            "audit_time":
            report.submitted_at.strftime("%H:%M:%S"),


            "auditor_id":
            report.auditor_id,


            "decision":
            report.audit_decision

        })


    return jsonify({

        "success":True,
        "total_reports":len(data),
        "reports":data

    })