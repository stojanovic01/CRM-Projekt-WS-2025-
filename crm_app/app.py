# app.py
from flask import Flask, render_template
from models import db
from views.customers import customers_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # erstellt Tabellen automatisch
    app.run(debug=True)

app.register_blueprint(customers_bp)
