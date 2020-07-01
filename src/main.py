"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db
from models import User, Client, Transaction, Special_Codes
#f rom models import Person
# TO HASH PASSWORD
# from passlib.apps import custom_app_context as pwd_context
# TO AUTHENTICATE USER LOGIN INFO
#from flask_httpauth import HTTPBasicAuth
#auth = HTTPBasicAuth()

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
@app.route('/user/create', methods=['POST'])
def new_user():
    name = request.json['name']
    email = request.json['email'] 
    password = request.json['password']
    qb_id = request.json['qb_id']
    if name is None or email is None or password is None or qb_id is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    new_user = User(name, email, password, qb_id)
    #user.hash_password(password)
    db.session.add(new_user)
    db.session.commit()

    response_body = {
        'msg': 'New user account has been activated.'
    }

    # redirect to user's account/login page?
    return jsonify(response_body), 200

# LOG IN TO USER ACCOUNT
@app.route('/user/login', methods=['GET'])
# def login():
    # body = request.get_json()
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        # print('Invalid username/email/password')
        return False 
    g.user = user
    return True
 
    response_body = {

    }
    # redirects to user's account home page/select client page
    return jsonify(response_body), 200

# SELECT CLIENT
@app.route('/client/', methods=['GET'])
def select_client(client_id):
    client = Client.query.get(client_id)

    redirect(url_for('/client/<client_id>')) 
    
    response_body = {

    }
    #redirect to '/client/client_id>
    return jsonify(response_body), 200


# REQUEST INFORMATION FROM CLIENT
@app.route('/client/<client_id>', methods=['GET'])
def request_info():
    unknowns = Transaction.query.filter_by(vendor_qb_id='Special_Codes.code' or customer_qb_id='Special_Codes.code' or GL_acct = 'Special_Codes.code').all()
    
    response_body = {
        'unspecified_transactions': 'unknowns'
    }
    # send email to client?
    return jsonify(response_body), 200

# CLIENT UPDATES UNKNOWN FIELDS
@app.route('/transaction/<transaction_id>', methods=['PUT'])
def update_transaction():
    transaction = Transaction.query.get(transaction_id)

    vendor_qb_id = request.json['vendor_qb_id']
    customer_qb_id = request.json['customer_qb_id']
    GL_acct = request.json['GL_acct']

    transaction.vendor_qb_id = vendor_qb_id
    transaction.customer_qb_id = customer_qb_id
    transaction.GL_acct = GL_acct

    db.session.commit()

    request_body = {
        'msg': 'Transaction information has been successfully updated.'
    }

    #send user_id email that client has responded
    return jsonify(request_body), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


    # all_transactions = Transactions.query.all()
    # unknowns = []
    # for transaction in all_transactions:
    #     if vendor_qb_id = Special_Codes.code or customer_qb_id = Special_Codes.code or GL_acct = Special_Codes.code
    #         unknowns.append(transaction)