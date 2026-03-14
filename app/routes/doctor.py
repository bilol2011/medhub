from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import Doctor, User, Appointment
from app import db
from app.forms import AppointmentForm
from flask_login import current_user, login_required

bp = Blueprint('doctor', __name__)

@bp.route('/list')
def list_doctors():
    category = request.args.get('category')
    query = request.args.get('q')
    
    doctors_query = Doctor.query.join(User)
    
    if category:
        doctors_query = doctors_query.filter(Doctor.specialty == category)
    
    if query:
        doctors_query = doctors_query.filter(
            (User.username.ilike(f'%{query}%')) | 
            (Doctor.specialty.ilike(f'%{query}%'))
        )
        
    doctors = doctors_query.all()
    return render_template('doctors/list.html', doctors=doctors, category=category, query=query)

@bp.route('/<int:id>')
def profile(id):
    doctor = Doctor.query.get_or_404(id)
    return render_template('doctors/profile.html', doctor=doctor)

@bp.route('/book/<int:id>', methods=['GET', 'POST'])
@login_required
def book_appointment(id):
    doctor = Doctor.query.get_or_404(id)
    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=current_user.id,
            doctor_id=doctor.id,
            datetime=form.datetime.data,
            reason=form.reason.data,
            status='pending'
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Sizning uchrashuv so‘rovingiz yuborildi!')
        return redirect(url_for('main.profile'))
    return render_template('appointments/book.html', doctor=doctor, form=form)

@bp.route('/appointment/<int:id>/<action>')
@login_required
def manage_appointment(id, action):
    appointment = Appointment.query.get_or_404(id)
    # Security check: only the doctor for this appointment can manage it
    if current_user.role != 'doctor' or appointment.doctor_id != current_user.doctor_profile.id:
        flash('Sizda ushbu amalni bajarish uchun ruxsat yo‘q.')
        return redirect(url_for('main.profile'))
    
    if action == 'confirm':
        appointment.status = 'confirmed'
        flash('Uchrashuv tasdiqlandi!')
    elif action == 'cancel':
        appointment.status = 'cancelled'
        flash('Uchrashuv bekor qilindi.')
    
    db.session.commit()
    return redirect(url_for('main.profile'))
