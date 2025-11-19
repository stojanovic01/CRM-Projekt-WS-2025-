#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WSGI-Einstiegspunkt für Phusion Passenger (Shared Hosting)
Diese Datei wird vom Webserver verwendet, um die Flask-App zu starten
"""

import sys
import os

# Pfad zum Anwendungsverzeichnis
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)

# Virtuelles Environment aktivieren (falls vorhanden)
# INTERP = os.path.join(os.environ.get('HOME', '/home/u243204db2'), 'venv', 'bin', 'python3')
# if os.path.isfile(INTERP):
#     exec(open(INTERP).read())

# Flask-App importieren
from app import app as application

# Für Debugging (auf Produktion auf False setzen!)
application.debug = False

if __name__ == '__main__':
    application.run()
