#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CGI-Einstiegspunkt für Flask-Anwendung
Alternative zu WSGI, falls der Server kein Passenger hat
"""

import sys
import os
from wsgiref.handlers import CGIHandler

# Pfad zum Anwendungsverzeichnis
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)

# Flask-App importieren
from app import app

# CGI-Handler starten
if __name__ == '__main__':
    CGIHandler().run(app)
