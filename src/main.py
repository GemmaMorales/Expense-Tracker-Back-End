"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db
from models import User, Client, Transaction, Special_Codes
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# CREATE NEW USER ACCOUNT
@app.route('/user', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email'] 
    password = request.json['password']
    qb_id = request.json['qb_id']

    new_user = User(name, email, password, qb_id)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user), 200

# LOG IN TO USER ACCOUNT
@app.route('/user', methods=['GET'])
def login():
    error = None
    if valid_login(request.form['user_id'],
                request.form['password']):
        return log_the_user_in(request.form['user_id'])
        #redirect to user's account
    else:
        error = 'Invalid userid/password'
    
    return jsonify(response_body), 200

# SELECT CLIENT
@app.route('/client/<client_id>', methods=['GET'])
def select_client(client_id):
    client = Client.query.get(client_id)

    redirect(url_for(#client's quickbooks acct)) 
    return jsonify(client), 200


# REQUEST INFORMATION FROM CLIENT
@app.route('/transaction', methods=['GET'])
def request_info():
    all_transactions = Transactions.query.all()
    unknowns = []
    for transaction in all_transactions:
        if vendor_qb_id = Special_Codes.code or customer_qb_id = Special_Codes.code or GL_acct = Special_Codes.code
            unknowns.append(transaction)
    
    return jsonify(unknowns), 200

# CLIENT UPDATES UNKNOWN FIELDS
@app.route('/transaction<transaction_id>', methods=['PUT'])
def update_transaction():
    transaction = Transaction.query.get(transaction_id)

    vendor_qb_id = request.json['vendor_qb_id']
    customer_qb_id = request.json['customer_qb_id']
    GL_acct = request.json['GL_acct']

    transaction.vendor_qb_id = vendor_qb_id
    transaction.customer_qb_id = customer_qb_id
    transaction.GL_acct = GL_acct

    db.session.commit()

    #send user_id email that client has responded
    return jsonify(transaction), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
