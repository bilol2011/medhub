from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request
from app.models import Post, Doctor, Like, Comment
from flask_login import login_required, current_user
from app import db
from app.forms import CommentForm, EditDoctorForm

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    doctors = Doctor.query.limit(3).all()
    form = CommentForm()
    return render_template('index.html', title='Bosh sahifa', posts=posts, doctors=doctors, form=form)

@bp.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if like:
        db.session.delete(like)
    else:
        new_like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)
    db.session.commit()
    return redirect(url_for('main.index'))

@bp.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, post_id=post_id, author_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Sizning izohingiz qo‘shildi!')
    return redirect(url_for('main.index'))

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = None
    if current_user.role == 'doctor':
        form = EditDoctorForm()
        if form.validate_on_submit():
            current_user.doctor_profile.specialty = form.specialty.data
            current_user.doctor_profile.experience = int(form.experience.data)
            current_user.doctor_profile.consultation_fee = float(form.consultation_fee.data)
            current_user.bio = form.bio.data
            db.session.commit()
            flash('Sizning profilingiz yangilandi!')
            return redirect(url_for('main.profile'))
        elif request.method == 'GET':
            form.specialty.data = current_user.doctor_profile.specialty
            form.experience.data = str(current_user.doctor_profile.experience)
            form.consultation_fee.data = str(current_user.doctor_profile.consultation_fee)
            form.bio.data = current_user.bio
            
    return render_template('profile.html', user=current_user, form=form)
