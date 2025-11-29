"""Dump a few rows from the conversations table and show counts.

Run from the `crm_app` folder with the same interpreter you run the app with.
Example:
  python scripts/dump_conversations.py
"""
import os
import sqlite3
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
DB_PATH = APP_DIR / 'instance' / 'crm.db'

def main():
    print('Using DB path:', DB_PATH)
    if not DB_PATH.exists():
        print('Database file does not exist.')
        return

    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    try:
        cur.execute("SELECT count(*) FROM conversations")
        total = cur.fetchone()[0]
        print('conversations count:', total)

        cur.execute("SELECT id, customer_id, user_id, channel, subject, conversation_time FROM conversations ORDER BY conversation_time DESC LIMIT 10")
        rows = cur.fetchall()
        if not rows:
            print('No rows in conversations table.')
        else:
            print('\nLatest conversations (up to 10):')
            for r in rows:
                print(r)
    except Exception as e:
        print('Error reading conversations table:', e)
    finally:
        conn.close()

if __name__ == '__main__':
    main()
