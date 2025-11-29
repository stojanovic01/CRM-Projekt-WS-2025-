import sys
import os
# ensure parent folder (crm_app) is on sys.path so imports like `from app import app` work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import Conversation, Customer
from sqlalchemy import or_, cast, String

with app.app_context():
    q = Conversation.query.join(Customer).filter(
        or_(
            cast(Conversation.channel, String).ilike('%A%'),
            Customer.first_name.ilike('%A%')
        )
    )
    print('matches:', q.count())
