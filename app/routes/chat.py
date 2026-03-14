from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Message, User
from app import db, socketio
from flask_socketio import emit, join_room, leave_room

bp = Blueprint('chat', __name__)

@bp.route('/')
@login_required
def index():
    # Show active chats
    sent_messages = Message.query.filter_by(sender_id=current_user.id).all()
    received_messages = Message.query.filter_by(recipient_id=current_user.id).all()
    contact_ids = set([m.recipient_id for m in sent_messages] + [m.sender_id for m in received_messages])
    contacts = User.query.filter(User.id.in_(contact_ids)).all()
    return render_template('chat/index.html', contacts=contacts)

@bp.route('/<int:recipient_id>')
@login_required
def room(recipient_id):
    recipient = User.query.get_or_404(recipient_id)
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.recipient_id == recipient_id)) |
        ((Message.sender_id == recipient_id) & (Message.recipient_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()
    return render_template('chat/room.html', recipient=recipient, messages=messages)

@socketio.on('message')
def handle_message(data):
    recipient_id = data['recipient_id']
    content = data['message']
    
    msg = Message(sender_id=current_user.id, recipient_id=recipient_id, content=content)
    db.session.add(msg)
    db.session.commit()
    
    room = f"user_{recipient_id}"
    emit('new_message', {
        'sender_id': current_user.id,
        'message': content,
        'timestamp': msg.timestamp.strftime('%H:%M')
    }, room=room)
    
    # Also send back to self to confirm
    emit('new_message', {
        'sender_id': current_user.id,
        'message': content,
        'timestamp': msg.timestamp.strftime('%H:%M')
    }, room=f"user_{current_user.id}")

@socketio.on('join')
def on_join(data):
    room = f"user_{current_user.id}"
    join_room(room)

@socketio.on('leave')
def on_leave(data):
    room = f"user_{current_user.id}"
    leave_room(room)
