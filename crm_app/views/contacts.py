from flask import Blueprint, render_template, request, session, redirect, url_for
from datetime import datetime
from crm_app.models import db, Conversation, Customer, User

contacts_bp = Blueprint('contacts', __name__, url_prefix='/contacts')

@contacts_bp.route('/')
def list_conversations():
    if db is None or Conversation is None:
        return "Fehler: Datenbankmodelle nicht verfügbar", 500

    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    try:
        channel = request.args.get('channel', '')
        query = Conversation.query

        if channel:
            query = query.filter_by(channel=channel)

        conversations = query.order_by(Conversation.conversation_time.desc()).all()
        return render_template('conversations.html', conversations=conversations, channel=channel)
    except Exception as e:
        print(f"list_conversations Fehler: {e}")
        return "Interner Fehler beim Laden der Gespräche", 500

@contacts_bp.route('/<int:conversation_id>')
def conversation_detail(conversation_id):
    if db is None or Conversation is None:
        return "Fehler: Datenbankmodelle nicht verfügbar", 500

    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    try:
        conversation = Conversation.query.get_or_404(conversation_id)
        return render_template('conversation_detail.html', conversation=conversation)
    except Exception as e:
        print(f"conversation_detail Fehler: {e}")
        return "Interner Fehler beim Laden des Gesprächs", 500

@contacts_bp.route('/add', methods=['GET', 'POST'])
def add_conversation():
    if db is None or Conversation is None or Customer is None:
        return "Fehler: Datenbankmodelle nicht verfügbar", 500

    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    try:
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
    except Exception as e:
        print(f"add_conversation Fehler: {e}")
        return "Interner Fehler beim Erstellen des Gesprächs", 500
