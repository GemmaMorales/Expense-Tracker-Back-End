import os
from flask_admin import Admin
from models import db, User, Client, Transaction, Special_Codes
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Expense Tracker', template_mode='bootstrap3')

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Client, db.session))
    admin.add_view(ModelView(Transaction, db.session))
    admin.add_view(ModelView(Special_Codes, db.session))