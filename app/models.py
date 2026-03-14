from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='patient') # 'patient' or 'doctor'
    bio = db.Column(db.Text)
    profile_pic = db.Column(db.String(256))
    
    # Relationships
    doctor_profile = db.relationship('Doctor', backref='user', uselist=False)
    appointments_as_patient = db.relationship('Appointment', backref='patient', lazy='dynamic', foreign_keys='Appointment.patient_id')
    messages_sent = db.relationship('Message', backref='sender', lazy='dynamic', foreign_keys='Message.sender_id')
    messages_received = db.relationship('Message', backref='recipient', lazy='dynamic', foreign_keys='Message.recipient_id')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    likes = db.relationship('Like', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def chat_rooms(self):
        # Find unique users who have sent or received messages from this user
        sent = Message.query.filter_by(sender_id=self.id).all()
        received = Message.query.filter_by(recipient_id=self.id).all()
        contact_ids = set([m.recipient_id for m in sent] + [m.sender_id for m in received])
        return User.query.filter(User.id.in_(contact_ids)).all()

    def __repr__(self):
        return f'<User {self.username}>'

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    specialty = db.Column(db.String(100), index=True)
    experience = db.Column(db.Integer) # years
    consultation_fee = db.Column(db.Float)
    rating = db.Column(db.Float, default=0.0)
    
    # Appointments as doctor
    appointments = db.relationship('Appointment', backref='doctor', lazy='dynamic', foreign_keys='Appointment.doctor_id')

    def __repr__(self):
        return f'<Doctor {self.specialty}>'

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    datetime = db.Column(db.DateTime, index=True)
    status = db.Column(db.String(20), default='pending') # pending, confirmed, completed, cancelled
    reason = db.Column(db.String(256))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    content = db.Column(db.Text)
    image = db.Column(db.String(256))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='post', lazy='dynamic', cascade='all, delete-orphan')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
