from flask import Blueprint, render_template, request, redirect, url_for, session
from crm_app.models import db, Conversation, Customer
from sqlalchemy import or_, cast, String
from math import ceil
import traceback

conversations_bp = Blueprint("conversations", __name__, url_prefix="/conversations")

# ---------------------------------------
# Route: Alle Konversationen auflisten
# ---------------------------------------
@conversations_bp.route("/")
def list_conversations():
    # Sicherstellen, dass der User eingeloggt ist
    if "user_id" not in session:
        return redirect(url_for("login.login"))

    # Filter- / Suchparameter
    search_q = request.args.get("q", "").strip()
    selected_channel = request.args.get("channel", "")
    current_order = request.args.get("order", "desc")
    page = request.args.get("page", 1, type=int)
    per_page = 20

    try:
        # Grundquery mit LEFT JOIN auf Customer
        query = Conversation.query.outerjoin(Customer)

        # ----------------------------
        #   Globale Suche
        # ----------------------------
        if search_q:
            pattern = f"%{search_q}%"
            query = query.filter(
                or_(
                    cast(Conversation.id, String).ilike(pattern),  # ID durchsuchen
                    Customer.first_name.ilike(pattern),           # Vorname
                    Customer.last_name.ilike(pattern),            # Nachname
                    Conversation.subject.ilike(pattern),          # Betreff
                    Conversation.notes.ilike(pattern),            # Notizen
                    Conversation.channel.ilike(pattern)           # Kanal
                )
            )

        # Kanal-Filter
        if selected_channel:
            query = query.filter(Conversation.channel == selected_channel)

        # Sortierung
        if current_order == "asc":
            query = query.order_by(Conversation.conversation_time.asc())
        else:
            query = query.order_by(Conversation.conversation_time.desc())

        # Pagination
        conversations_pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        # Kanalliste
        channels = ["Telefon", "E-Mail", "Meeting", "Chat"]

        # Template rendern
        return render_template(
            "conversations.html",
            conversations_pagination=conversations_pagination,
            search_q=search_q,
            selected_channel=selected_channel,
            current_order=current_order,
            channels=channels
        )

    except Exception as e:
        # Stacktrace für Logs ausgeben
        print("Fehler in list_conversations:", e)
        traceback.print_exc()
        return f"Interner Fehler: {e}", 500


# ---------------------------------------
# Route: Konversationen eines Kunden
# ---------------------------------------
@conversations_bp.route("/customer/<int:customer_id>/")
def customer_conversations(customer_id):
    if "user_id" not in session:
        return redirect(url_for("login.login"))

    # Kunde abrufen oder 404
    customer = Customer.query.get_or_404(customer_id)

    # Alle Konversationen des Kunden, neueste zuerst
    conversations = Conversation.query.filter_by(customer_id=customer_id)\
                                      .order_by(Conversation.conversation_time.desc())\
                                      .all()

    # Template rendern
    return render_template(
        "customer_conversations.html",
        customer=customer,
        conversations=conversations
    )
