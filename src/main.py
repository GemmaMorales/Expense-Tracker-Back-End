"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, datetime
from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db
from models import User, Client, Transaction, Special_Codes
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)
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
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

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
    if 'name' not in request.json:
        raise APIException('You need to specify the name', status_code=400)
    if 'email' not in request.json:
        raise APIException('You need to specify the name', status_code=400)
    if 'password' not in request.json:
        raise APIException('You need to specify the name', status_code=400)
    name = request.json['name']
    email = request.json['email'] 
    password = request.json['password']

    print(request.json)
   
    if User.query.filter_by(email =email).first() is not None:
        raise APIException('An account already exists for this email', status_code=400)
    new_user = User(name=name, email=email, password=password)
    #user.hash_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 200

# LOG IN TO USER ACCOUNT
@app.route('/token', methods=['POST'])
def login():
    body = request.get_json()
    if 'email' not in body:
        raise APIException('Please specify a email', status_code=400)
    if 'password' not in body:
        raise APIException('Please specify a password', status_code=400)
    user = User.query.filter_by(email = body["email"], password=body['password']).first()
    ret = {'jwt': create_jwt(identity=user.user_id), 'user_id': user.user_id}
    return jsonify(ret), 200

# SELECT CLIENT
@app.route('/client/<int:client_id>/transactions', methods=['GET'])
def select_client(client_id):
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
        transaction.vendor_qb_id = request.json["customer_qb_id"]
    if "GL_acct" in request.json: 
        transaction.vendor_qb_id = request.json["GL_acct"]


    db.session.commit()

    return jsonify(transaction.serialize()), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


    # all_transactions = Transactions.query.all()
    # unknowns = []
    # for transaction in all_transactions:
    #     if vendor_qb_id = Special_Codes.code or customer_qb_id = Special_Codes.code or GL_acct = Special_Codes.code
    #         unknowns.append(transaction)