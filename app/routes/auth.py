from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app import db
from app.models import Auditor



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

@auth_bp.route('/auditor_dashboard')
def auditor_dashboard():
    if 'auditor' in session:
        return render_template('auditor_dashboard.html')
    else:
        return redirect(url_for('auth.login'))





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

