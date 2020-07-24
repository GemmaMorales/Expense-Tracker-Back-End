from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(60))
    qb_code = db.Column(db.String(255), unique=True)
    qb_realmID = db.Column(db.String(255)) 
    
    
    client = db.relationship ("Client")
    special_codes = db.relationship ("Special_Codes")

  
    def serialize(self):
        return {
            "user_id": self.user_id,
            "password": self.password,
            "name": self.name,
            "email": self.email
        }

class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True, unique=True)
    company_name = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    email = db.Column(db.String(200), unique=True)

    transactions = db.relationship ("Transaction")

    def serialize(self):
        return {
            "client_id": self.client_id,
            "company_name": self.company_name,
            "user_id": self.user_id,
            "email": self.email
        }

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True, unique=True)
    client_id = db.Column(db.Integer, db.ForeignKey(Client.client_id))
    date = db.Column(db.Date)
    amount = db.Column(db.Float)
    transaction_type = db.Column(db.Enum("expense","revenue"))
    vendor_qb_id = db.Column(db.String(200))
    customer_qb_id = db.Column(db.String(200))
    GL_acct = db.Column(db.Integer)
    transaction_description = db.Column(db.String(255))
    payee_or_payer = db.Column(db.String(200))

    def serialize(self):
        client = Client.query.get(self.client_id)
        if client is not None:
            client = client.serialize()
        return {
            "client": client,
            "transaction_id": self.transaction_id,
            "date": self.date,
            "amount": self.amount,
            "transaction_type": self.transaction_type,
            "vendor_qb_id": self.vendor_qb_id,
            "customer_qb_id": self.customer_qb_id,
            "GL_acct": self.GL_acct,
            "transaction_description": self.transaction_description,
            "payee_or_payer": self.payee_or_payer
        }

class Special_Codes(db.Model):
    sc_id = db.Column(db.Integer, primary_key=True, unique=True)
    code_type = db.Column(db.Enum("vendor_name","customer_name","GL_acct"))
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    code = db.Column(db.String(200))
    

    def serialize(self):
        return {
            "code_type": self.code_type,
            "user_id": self.user_id,
            "code": self.code
        }

