"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, datetime
from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap, send_simple_message
from admin import setup_admin
from models import db
from models import User, Client, Transaction, Special_Codes
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)
from quickbooks import add_endpoints

app = Flask(__name__)
app.url_map.strict_slashes = False
app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)
app = add_endpoints(app) 


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
def new_user():
    if request.is_json == False:
        raise APIException('The request must contain a json', status_code=400)
    if 'name' not in request.json:
        raise APIException('You need to specify the name', status_code=400)
    if 'email' not in request.json:
        raise APIException('You need to specify the email', status_code=400)
    if 'password' not in request.json:
        raise APIException('You need to specify the password', status_code=400)
    name = request.json['name']
    email = request.json['email'] 
    password = request.json['password']

    print(request.json)
   
    if User.query.filter_by(email =email).first() is not None:
        raise APIException('An account already exists for this email', status_code=400)
    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 200

# LOG IN TO USER ACCOUNT
@app.route('/token', methods=['POST'])
def login():
    if request.is_json == False:
        raise APIException('The request must be in json format', status_code=400)
    body = request.get_json()
    if 'email' not in body:
        raise APIException('Please specify an email', status_code=400)
    if 'password' not in body:
        raise APIException('Please specify a password', status_code=400)
    user = User.query.filter_by(email = body["email"], password=body['password']).first()
    if user is None:
        raise APIException('Invalid username or password')
    ret = {'jwt': create_jwt(identity=user.user_id), 'user_id': user.user_id}
    return jsonify(ret), 200

# GENERATE CLIENT LIST
@app.route('/clients', methods=['GET'])
def get_clients():
    # vendor_qb_id = request.args.get('vendor_qb_id')
    # customer_qb_id = request.args.get('customer_qb_id')
    # GL_acct = request.args.get('GL_acct')
    clients = Client.query.all() 
    # if vendor_qb_id is not None:
    #     transactions = transactions.filter_by(vendor_qb_id=vendor_qb_id)
    # if customer_qb_id is not None:
    #     transactions = transactions.filter_by(customer_qb_id=customer_qb_id)
    # if GL_acct is not None:
    #     transactions = transactions.filter_by(GL_acct=GL_acct)
    serialized_clients = list(map(lambda x: x.serialize(), clients))
    return jsonify(serialized_clients), 200

# SELECT CLIENT AND GET TRANSACTIONS
@app.route('/client/<int:client_id>/transactions', methods=['GET'])
def select_client_transactions(client_id):
    vendor_qb_id = request.args.get('vendor_qb_id')
    customer_qb_id = request.args.get('customer_qb_id')
    GL_acct = request.args.get('GL_acct')
    transactions = Transaction.query.filter_by(client_id=client_id)   
    if vendor_qb_id is not None:
        transactions = transactions.filter_by(vendor_qb_id=vendor_qb_id)
    if customer_qb_id is not None:
        transactions = transactions.filter_by(customer_qb_id=customer_qb_id)
    if GL_acct is not None:
        transactions = transactions.filter_by(GL_acct=GL_acct)
    serialized_transactions = list(map(lambda x: x.serialize(), transactions))
    return jsonify(serialized_transactions), 200

#TESTING
@app.route('/transactions', methods=['GET'])
def post_transaction():
    tran1 = Transaction(
        
            client_id = 1,
            date = datetime.date.today(),
            amount = 4.00,
            transaction_type = 'revenue',
            vendor_qb_id = 6123,
            customer_qb_id = 124,
            GL_acct = 7823
    )
    db.session.add(tran1)
    db.session.commit()



# CLIENT UPDATES TRANSACTION
@app.route('/transaction/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if transaction is None:
        raise APIException('Transaction not found.', status_code=404)
    if "vendor_qb_id" in request.json: 
        transaction.vendor_qb_id = request.json["vendor_qb_id"]
    if "customer_qb_id" in request.json: 
        transaction.customer_qb_id = request.json["customer_qb_id"]
    if "GL_acct" in request.json: 
        transaction.GL_acct = request.json["GL_acct"]
    db.session.commit()

    return jsonify(transaction.serialize()), 200


#DECODE OBJECT RESPONSE FOR TRNSACTION DESCRIPTION
@app.route('/transactions/descriptions', methods=['PUT'])
def decode_response():
    if request.is_json == False:
        raise APIException('The request must be in json format', status_code=400)
    body = request.get_json()
    client_id=None
    for key, value in body.items():
        transaction = Transaction.query.get(key)
        transaction.transaction_description = value  
        print(transactions.serialize())
        client_id=transaction.client_id
    db.session.commit()
    client = Client.query.get(client_id)
    send_simple_message(client.email, "Please provide missing details to the transactions listed", "Please provide missing details to the transactions listed below:")
    return "okay", 200 

      
#DECODE OBJECT RESPONSE FOR VENDOR/CUSTOMER NAME
@app.route('/transactions/payees_or_payers', methods=['PUT'])
def decode_transaction_descriptions_response():
    if request.is_json == False:
        raise APIException('The request must be in json format', status_code=400)
    body = request.get_json()
    for key, value in body.items():
        transaction = Transaction.query.get(key)
        payee_or_payer = value  
    db.session.commit()
    return "okay", 200  
    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


