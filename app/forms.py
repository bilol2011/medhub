from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    login_id = StringField('Username yoki email', validators=[DataRequired()])
    password = PasswordField('Parol', validators=[DataRequired()])
    submit = SubmitField('Kirish')

class RegistrationForm(FlaskForm):
    username = StringField('Foydalanuvchi nomi', validators=[DataRequired()])
    email = StringField('Email manzili', validators=[DataRequired(), Email()])
    password = PasswordField('Parol', validators=[DataRequired()])
    password2 = PasswordField('Parolni takrorlang', validators=[DataRequired(), EqualTo('password')])
    profile_pic = FileField('Profil rasmi', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Faqat rasmlar yuklash mumkin!')])
    submit = SubmitField('Ro‘yxatdan o‘tish')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Ushbu foydalanuvchi nomi band. Iltimos, boshqasini tanlang.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Ushbu email manzili band. Iltimos, boshqasini tanlang.')

class StaffRegistrationForm(RegistrationForm):
    role = SelectField('Ro‘yxatdan o‘tish turi', choices=[('doctor', 'Shifokor'), ('admin', 'Admin')], validators=[DataRequired()])
    specialty = SelectField('Mutaxassislik', choices=[('Kardiologiya', 'Kardiologiya'), ('Stomatologiya', 'Stomatologiya'), ('Dermatologiya', 'Dermatologiya'), ('Nevrologiya', 'Nevrologiya'), ('Pediatriya', 'Pediatriya'), ('Ortopediya', 'Ortopediya')])
    experience = StringField('Tajriba (yillarda)')
    consultation_fee = StringField('Konsultatsiya narxi ($)')


class AppointmentForm(FlaskForm):
    datetime = DateTimeField('Qabul vaqti (YYYY-MM-DD HH:MM)', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    reason = TextAreaField('Qabul sababi', validators=[DataRequired()])
    submit = SubmitField('Uchrashuvni band qilish')

class PostForm(FlaskForm):
    title = StringField('Sarlavha', validators=[DataRequired()])
    content = TextAreaField('Matn', validators=[DataRequired()])
    submit = SubmitField('Chop etish')

class CommentForm(FlaskForm):
    content = TextAreaField('Izoh', validators=[DataRequired()])
    submit = SubmitField('Yuborish')

class EditDoctorForm(FlaskForm):
    specialty = SelectField('Mutaxassislik', choices=[('Kardiologiya', 'Kardiologiya'), ('Stomatologiya', 'Stomatologiya'), ('Dermatologiya', 'Dermatologiya'), ('Nevrologiya', 'Nevrologiya'), ('Pediatriya', 'Pediatriya'), ('Ortopediya', 'Ortopediya')], validators=[DataRequired()])
    experience = StringField('Tajriba (yillarda)', validators=[DataRequired()])
    consultation_fee = StringField('Konsultatsiya narxi ($)', validators=[DataRequired()])
    bio = TextAreaField('Men haqimda (ixtiyoriy)')
    submit = SubmitField('Profilni yangilash')
