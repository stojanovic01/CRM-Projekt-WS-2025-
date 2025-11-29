from flask import Blueprint, render_template, request, session, redirect, url_for
from crm_app.models import db, Conversation, Customer, User
from datetime import datetime

contacts_bp = Blueprint('contacts', __name__, url_prefix='/contacts')

@contacts_bp.route('/')
def list_conversations():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))
    
    # Filter nach Kanal
    channel = request.args.get('channel', '')
    
    query = Conversation.query
    
    if channel:
        query = query.filter_by(channel=channel)
    
    conversations = query.order_by(Conversation.conversation_time.desc()).all()
    
    return render_template('conversations.html', conversations=conversations, channel=channel)

@contacts_bp.route('/<int:conversation_id>')
def conversation_detail(conversation_id):
    if 'user_id' not in session:
        return redirect(url_for('login.login'))
    
    conversation = Conversation.query.get_or_404(conversation_id)
    
    return render_template('conversation_detail.html', conversation=conversation)

@contacts_bp.route('/add', methods=['GET', 'POST'])
def add_conversation():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))
    
    if request.method == 'POST':
        conversation = Conversation(
            customer_id=request.form.get('customer_id'),
            user_id=session.get('user_id'),
            channel=request.form.get('channel'),
            subject=request.form.get('subject'),
            notes=request.form.get('notes'),
            conversation_time=datetime.now()
        )
        db.session.add(conversation)
        db.session.commit()
        return redirect(url_for('contacts.list_conversations'))
    
    customers = Customer.query.all()
    return render_template('conversation_form.html', customers=customers)