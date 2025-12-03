from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime

# Modelle laden – mit Fallbacks (wie in deinen anderen Dateien)
try:
    from crm_app.models import db, Customer, Conversation
except ModuleNotFoundError:
    try:
        from ..models import db, Customer, Conversation
    except ModuleNotFoundError:
        try:
            from models import db, Customer, Conversation
        except ModuleNotFoundError:
            db = None
            Customer = None
            Conversation = None
            print("⚠️ Warning: Konversationsmodelle konnten nicht importiert werden!")

conversations_bp = Blueprint("conversations", __name__, url_prefix="/conversations")


# -------------------------------------
#  ALLE KONVERSATIONEN LISTEN
# -------------------------------------
@conversations_bp.route("/")
def list_conversations():
    if db is None or Conversation is None:
        return "Fehler: Datenbankmodelle nicht verfügbar", 500

    if "user_id" not in session:
        return redirect(url_for("login.login"))

    try:
        conversations = Conversation.query.order_by(
            Conversation.conversation_time.desc()
        ).all()

        return render_template(
            "conversations.html",
            conversations=conversations
        )
    except Exception as e:
        print(f"list_conversations Fehler: {e}")
        return "Interner Fehler beim Laden der Konversationen", 500


# -------------------------------------
#  KONVERSATION FÜR EINEN KONKRETEN KUNDEN
# -------------------------------------
@conversations_bp.route("/customer/<int:customer_id>")
def customer_conversations(customer_id):
    if db is None or Conversation is None or Customer is None:
        return "Fehler: Datenbankmodelle nicht verfügbar", 500

    if "user_id" not in session:
        return redirect(url_for("login.login"))

    try:
        customer = Customer.query.get_or_404(customer_id)

        conversations = Conversation.query.filter_by(
            customer_id=customer_id
        ).order_by(
            Conversation.conversation_time.desc()
        ).all()

        return render_template(
            "customer_conversations.html",
            customer=customer,
            conversations=conversations
        )

    except Exception as e:
        print(f"customer_conversations Fehler: {e}")
        return "Interner Fehler beim Laden der Kundenkonversationen", 500


# -------------------------------------
#  NEUE KONVERSATION HINZUFÜGEN
# -------------------------------------
@conversations_bp.route("/add/<int:customer_id>", methods=["GET", "POST"])
def add_conversation(customer_id):
    if db is None or Conversation is None or Customer is None:
        return "Fehler: Datenbankmodelle nicht verfügbar", 500

    if "user_id" not in session:
        return redirect(url_for("login.login"))

    try:
        customer = Customer.query.get_or_404(customer_id)

        if request.method == "POST":
            conversation_text = request.form.get("conversation_text")

            if not conversation_text.strip():
                return "Konversationstext darf nicht leer sein", 400

            new_conversation = Conversation(
                customer_id=customer_id,
                conversation_text=conversation_text,
                conversation_time=datetime.now(),
            )

            db.session.add(new_conversation)
            db.session.commit()

            return redirect(url_for("conversations.customer_conversations", customer_id=customer_id))

        return render_template(
            "add_conversation.html",
            customer=customer
        )

    except Exception as e:
        print(f"add_conversation Fehler: {e}")
        return "Interner Fehler beim Erstellen der Konversation", 500
