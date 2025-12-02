from crm_app.models import db, User
from flask import Blueprint, render_template, request, session, redirect, url_for, flash

login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    error = None
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            if not email or not password:
                error = 'Bitte E-Mail und Passwort eingeben.'
            else:
                user = User.query.filter_by(email=email).first()
                if not user:
                    error = 'Benutzer existiert nicht.'
                elif user.password_hash != password:
                    error = 'Ungültiges Passwort.'
                else:
                    # Login erfolgreich
                    session['user_id'] = user.id
                    session['user_name'] = user.name
                    return redirect(url_for('firstpage'))

    except Exception as e:
        error = f'Ein interner Fehler ist aufgetreten: {e}'

    return render_template('login.html', error=error)

@login_bp.route('/logout')
def logout():
    try:
        session.clear()
        flash('Logout erfolgreich.')
    except Exception as e:
        flash(f'Fehler beim Logout: {e}')
    return redirect(url_for('login.login'))
