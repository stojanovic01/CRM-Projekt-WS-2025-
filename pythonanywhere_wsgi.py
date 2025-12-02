import sys
import os
from dotenv import load_dotenv

# Projektpfad
project_root = '/home/sstojanovi/mysite'
sys.path.insert(0, project_root)

# Virtualenv-Pfad
venv_path = '/home/sstojanovi/.virtualenvs/mysite-312'
activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')
if os.path.exists(activate_this):
    with open(activate_this) as f:
        exec(f.read(), {'__file__': activate_this})

# Optional: ins Projektverzeichnis wechseln
os.chdir(project_root)

# .env laden
load_dotenv(os.path.join(project_root, '.env'))
os.environ['FLASK_ENV'] = 'production'

# Flask-App importieren
from app import app as application
