"""Seed script: populate `conversations` table with dummy conversations.

This script is safe to run from the repository root or from the `crm_app` folder.
It will attach to the app's SQLAlchemy instance and create Conversation rows
that reference existing `Customer` and `User` rows.

Example (PowerShell):
    Set-Location -Path ".../crm_app"
    ./.venv/Scripts/Activate.ps1  # if you use a venv
    python scripts/seed_conversations.py

By default the script will not add conversations if rows already exist. Use
`force=True` to always add rows.
"""
import os
import sys

# Make imports  work regardless of current working directory when running the script.
# Ensure the `crm_app` folder (the parent of this scripts/ folder) is on sys.path so
# `from app import app, db` works.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(SCRIPT_DIR)
if APP_DIR not in sys.path:
        sys.path.insert(0, APP_DIR)
from datetime import datetime, timedelta
import random

from app import app, db
from models import Customer, Conversation, User


def make_dummy_notes():
    choices = [
        'Kunde zeigt großes Interesse an unserer Premium-Lösung. Nächster Schritt: Angebot.',
        'Technische Fragen beantwortet. Kunde prüft intern.',
        'Follow-up nach Meeting: Bitte Demo vereinbaren.',
        'Support-Anfrage bearbeitet, Ticket geschlossen.',
        'Preisverhandlung läuft — Rabattanfrage gestellt.',
        'Termin wird vorbereitet, Präsentation nächste Woche.',
        'Beschwerde wegen Lieferverzug, Entschädigung vorgeschlagen.',
        'Kunde interessiert sich für Zusatzmodule (Cross-Sell).'
    ]
    return random.choice(choices)


def seed(conversations_per_customer_min=1, conversations_per_customer_max=3, force=False):
    with app.app_context():
        # Ensure tables exist (safe: create_all is idempotent)
        db.create_all()
        existing = Conversation.query.count()
        if existing > 0 and not force:
            print(f"Abbruch: Es existieren bereits {existing} Konversation(en) in der Datenbank. Verwende force=True, um trotzdem zu erzeugen.")
            return

        customers = Customer.query.all()
        if not customers:
            print("Keine Kunden gefunden. Bitte zuerst Kunden in der DB anlegen (oder starte app.py, das Beispielkunden anlegt).")
            return

        # prefer an admin or any user to reference as user_id
        user = User.query.filter_by(name='administrator').first() or User.query.first()
        if not user:
            # create a simple user to associate with conversations
            user = User(name='seed_user', email='seed@local', password_hash='', role='Admin')
            db.session.add(user)
            db.session.commit()

        channels = ['Telefon', 'E-Mail', 'Meeting', 'Chat']
        subjects = [
            'Erstkontakt - Interesse an unseren Lösungen',
            'Nachfrage zu Produktdetails',
            'Vertragsverhandlung',
            'Support-Anfrage',
            'Follow-up nach Meeting',
            'Terminvereinbarung',
            'Beschwerde',
            'Angebotsnachfrage'
        ]

        created = 0
        for customer in customers:
            count = random.randint(conversations_per_customer_min, conversations_per_customer_max)
            for _ in range(count):
                days_ago = random.randint(0, 180)
                hours_ago = random.randint(0, 23)
                convo_time = datetime.now() - timedelta(days=days_ago, hours=hours_ago)

                c = Conversation(
                    customer_id=customer.id,
                    user_id=user.id,
                    channel=random.choice(channels),
                    subject=random.choice(subjects),
                    notes=make_dummy_notes(),
                    conversation_time=convo_time
                )
                db.session.add(c)
                created += 1

        db.session.commit()
        print(f"Erstellt: {created} Konversation(en) für {len(customers)} Kunden.")


if __name__ == '__main__':
    # change parameters here if needed
    seed(conversations_per_customer_min=1, conversations_per_customer_max=3, force=False)
