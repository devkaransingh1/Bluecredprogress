from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app import db
from app.models import Auditor

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template('landing.html')


#login route logic
@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if 'auditor' in session:
        return redirect(url_for('auth.industry_records',username=session['auditor']))
    if request.method=='POST':
        userId = request.form.get('blueId')
        userPassword = request.form.get('bluePass')
        auditor = Auditor.query.filter_by(blue_id=userId,password=userPassword).first()
        if auditor:
            session['auditor']=auditor.name
            return redirect(url_for('auth.industry_records',username = session['auditor']))
        else:
            flash('Invalid Blue ID or Password, Try again.','danger')
            return redirect(url_for('auth.login'))
    return render_template('login.html')



@auth_bp.route('/register')
def register():
    return render_template('register.html')


@auth_bp.route('/industry_records')
def industry_records():
    if 'auditor' in session:
        return render_template('industry_records.html',username=session['auditor'])
    else:
        return redirect(url_for('auth.login'))
    
@auth_bp.route('/logout')
def logout():
    session.pop('auditor',None)
    flash('Auditor logged out successfully','info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgotpassword')
def forgotpassword():
    return render_template('forgotpassword.html')