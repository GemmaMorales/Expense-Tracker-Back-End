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

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    password = Column(String)
    name = Column(String)
    email_address= Column(String)

class Client(Base):
    __tablename__ = "client"
    client_id = Column(Integer, primary_key=True)
    company_name = Column(String)
    bookkeeper = Column(Integer, ForeignKey("user.user_id"))
    email_address = Column(String)

class Transaction(Base):
    __tablename__ = "transaction"
    transaction_id = Column(Integer, primary_key=True)
    client = Column(Integer, ForeignKey("client.client_id"))
    date = Column(Date)
    amount = Column(Float)
    transaction_type = Column(Enum("expense","revenue"))
    name = Column(String)
    GL_account = Column(Integer)

class Unknown(Base):
    __tablename__ = "unknown"
    unknown_id = Column(Integer, primary_key=True)
    transaction = Column(Integer, ForeignKey(transaction.transaction_id))
    missing_entity = Column(Enum("vendor_name","customer_name","GL_acct"))
