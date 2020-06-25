from flask_sqlalchemy import SQLAlchemy

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
    user_id = db.Column(db.Integer, primary_key=True)
    qb_id = db.Column(db.Integer, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)

    clients = db.relationship ("Clients")
    special_codes = db.relationship ("Special_Codes")

    def serialize(self):
        return {
            "username": self.user_id,
            "password": self.password,
            "name": self.name,
            "email": self.email
        }

class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String)
    user_id = db.Column(db.Integer, ForeignKey("User.user_id"))
    email = db.Column(db.String, unique=True)

    transactions = db.relationship ("Transactions")

    def serialize(self):
        return {
            "client_id": self.client_id,
            "company_name": self.company_name,
            "user_id": self.user_id,
            "email": self.email
        }

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.Integer, ForeignKey("client.client_id"))
    date = db.Column(db.Date)
    amount = db.Column(db.Float)
    transaction_type = db.Column(db.Enum("expense","revenue"))
    vendor_qb_id = db.Column(db.String)
    customer_qb_id = db.Column(db.String)
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
    code_type = db.Column(db.Enum("vendor_name","customer_name","GL_acct"))
    user_id = db.Column(db.Integer, ForeignKey(User.user_id))
    code = db.Column(db.String)
    

    def serialize(self):
        return {
            "code_type": self.code_type,
            "user_id": self.user_id,
            "code": self.code
        }
