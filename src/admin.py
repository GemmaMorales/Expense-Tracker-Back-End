from flask_admin import Admin

def setup_admin(app):
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Expense Tracker', template_mode='bootstrap3')