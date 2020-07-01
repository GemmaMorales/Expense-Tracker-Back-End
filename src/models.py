from flask_sqlalchemy import SQLAlchemy
# from passlib.apps import custom_app_context as pwd_context

db = SQLAlchemy()

# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<Person %r>' % self.username

#     def serialize(self):
#         return {
#             "username": self.username,
#             "email": self.email
#         }

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    password#_hash = db.Column(db.String(60))
    qb_id = db.Column(db.Integer, unique=True)
    
    
    client = db.relationship ("Client")
    special_codes = db.relationship ("Special_Codes")

    #def set_password(self, password)
    
    # def hash_password(self, password):
    #     self.password_hash = pwd_context.encrypt(password)

    # def verify_password(self, password):
    #     return pwd_context.verify(password, self.password_hash)

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

    transaction = db.relationship ("Transaction")

    def serialize(self):
        return {
            "client_id": self.client_id,
            "company_name": self.company_name,
            "user_id": self.user_id,
            "email": self.email
        }

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True, unique=True)
    client = db.Column(db.Integer, db.ForeignKey(Client.client_id))
    date = db.Column(db.Date)
    amount = db.Column(db.Float)
    transaction_type = db.Column(db.Enum("expense","revenue"))
    vendor_qb_id = db.Column(db.String(200))
    customer_qb_id = db.Column(db.String(200))
    GL_acct = db.Column(db.Integer)

    def serialize(self):
        return {
            "transaction_id": self.transaction_id,
            "client": self.client,
            "date": self.namedate,
            "amount": self.amount,
            "transaction_type": self.transaction_type,
            "vendor_qb_id": self.vendor_qb_id,
            "customer_qb_id": self.customer_qb_id,
            "GL_acct": self.GL_acct
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
