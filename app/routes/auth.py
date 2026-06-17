from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app import db
from app.models import Auditor , Industry , IndustryAccess



auth_bp = Blueprint('auth', __name__)


# landing page route

@auth_bp.route('/')
def home():
    if 'auditor' in session:
        return redirect(url_for('auth.auditor_dashboard'))
    return render_template('landing.html')





#login page and logic route

@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if 'auditor' in session:
        return redirect(url_for('auth.auditor_dashboard'))
    if request.method=='POST':
        userId = request.form.get('blueId')
        userPassword = request.form.get('bluePass')
        auditor = Auditor.query.filter_by(blue_id=userId,password=userPassword).first()
        if auditor:
            session['auditor']=auditor.id
            return redirect(url_for('auth.auditor_dashboard'))
        else:
            flash('Invalid Blue ID or Password, Try again.','danger')
            return redirect(url_for('auth.login'))
    return render_template('login.html')




# registeration page route

@auth_bp.route('/register')
def register():
    return render_template('register.html')




# auditor after login dashboard route

@auth_bp.route('/auditor_dashboard', methods=['GET','POST'])
def auditor_dashboard():

    if 'auditor' not in session:
        return redirect(url_for('auth.login'))


    # auditor enters industry credentials
    if request.method == 'POST':
        industryid = request.form.get('siteCode')
        fvk = request.form.get('fieldKey')

        access = IndustryAccess.query.filter_by(
            industry_id=industryid,
            field_verification_key=fvk
        ).first()


        if access:

            industry = Industry.query.filter_by(
                industry_id=industryid
            ).first()


            if industry:

                # store selected industry
                session['loggedin_industry'] = industry.industry_id

                return render_template('audit_report.html')


        flash("Invalid Industry ID or Verification Key")
        return redirect(
            url_for('auth.auditor_dashboard')
        )
    return render_template('auditor_dashboard.html')




# after both industry and auditor verification done

@auth_bp.route('/audit_report')
def audit_report():
    print("industry id =", session.get('loggedin_industry'))
    if 'loggedin_industry' in session:
        return render_template('audit_report.html')

    return redirect(url_for('auth.auditor_dashboard'))




# auditor after logout route

@auth_bp.route('/logout')
def logout():
    session.pop('auditor',None)
    flash('Auditor logged out successfully','info')
    return redirect(url_for('auth.login'))




# auditor forgot password route

@auth_bp.route('/forgotpassword')
def forgotpassword():
    return render_template('forgotpassword.html')

