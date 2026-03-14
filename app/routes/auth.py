import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, current_user
from urllib.parse import urlsplit
from app import db
from app.forms import LoginForm, RegistrationForm, StaffRegistrationForm
from app.models import User, Doctor

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.username == form.login_id.data) | (User.email == form.login_id.data)).first()
        if user is None or not user.check_password(form.password.data):
            flash('Foydalanuvchi nomi/email yoki parol noto‘g‘ri')
            return redirect(url_for('auth.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Kirish', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role='patient')
        user.set_password(form.password.data)
        
        if hasattr(form, 'profile_pic') and form.profile_pic.data:
            pic_filename = secure_filename(f"{form.username.data}_{form.profile_pic.data.filename}")
            pic_path = os.path.join(current_app.root_path, 'static', 'uploads', 'profiles')
            os.makedirs(pic_path, exist_ok=True)
            form.profile_pic.data.save(os.path.join(pic_path, pic_filename))
            user.profile_pic = f"uploads/profiles/{pic_filename}"
            
        db.session.add(user)
        db.session.commit()
        flash('Tabriklaymiz, siz muvaffaqiyatli ro‘yxatdan o‘tdingiz!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Ro‘yxatdan o‘tish', form=form)

@bp.route('/register-staff', methods=['GET', 'POST'])
def register_staff():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = StaffRegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        
        if hasattr(form, 'profile_pic') and form.profile_pic.data:
            pic_filename = secure_filename(f"{form.username.data}_{form.profile_pic.data.filename}")
            pic_path = os.path.join(current_app.root_path, 'static', 'uploads', 'profiles')
            os.makedirs(pic_path, exist_ok=True)
            form.profile_pic.data.save(os.path.join(pic_path, pic_filename))
            user.profile_pic = f"uploads/profiles/{pic_filename}"

        db.session.add(user)
        db.session.flush() # Get user id
        
        if user.role == 'doctor':
            experience = int(form.experience.data) if form.experience.data else 0
            fee = float(form.consultation_fee.data) if form.consultation_fee.data else 0.0
            doctor = Doctor(user_id=user.id, specialty=form.specialty.data, experience=experience, consultation_fee=fee, rating=5.0)
            db.session.add(doctor)
            
        db.session.commit()
        flash('Tabriklaymiz, siz (shifokor/admin) muvaffaqiyatli ro‘yxatdan o‘tdingiz!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register_staff.html', title='Xodimlar uchun ro‘yxatdan o‘tish', form=form)
