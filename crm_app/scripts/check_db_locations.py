"""Check all crm.db files under the project and report whether the
`conversations` table exists and how many rows it contains.

Run with the same Python interpreter you use for the app/seed script. Example:
    C:/Users/stash/anaconda3/python.exe scripts/check_db_locations.py
"""
import os
import sqlite3
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def find_crm_dbs(root):
    matches = []
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            if f.lower() == 'crm.db':
                matches.append(os.path.join(dirpath, f))
    return sorted(set(matches))

def inspect_db(path):
    info = {}
    try:
        stat = os.stat(path)
        info['size'] = stat.st_size
        info['mtime'] = datetime.fromtimestamp(stat.st_mtime).isoformat()
    except Exception:
        info['size'] = None
        info['mtime'] = None

    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        # Check if conversations table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations';")
        tbl = cur.fetchone()
        if not tbl:
            info['conversations_exists'] = False
            info['conversations_count'] = 0
        else:
            info['conversations_exists'] = True
            cur.execute('SELECT count(*) FROM conversations')
            info['conversations_count'] = cur.fetchone()[0]
        conn.close()
    except Exception as e:
        info['error'] = str(e)

    return info

def main():
    print('Project root (detected):', ROOT)
    dbs = find_crm_dbs(ROOT)
    if not dbs:
        print('No crm.db files found under project root.')
        return

    for p in dbs:
        print('\n---')
        print('Path:', p)
        info = inspect_db(p)
        for k, v in info.items():
            print(f'{k}: {v}')

if __name__ == '__main__':
    main()
