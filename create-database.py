import sys
import sqlite3
from sqlalchemy import Table, create_engine
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


conn = sqlite3.connect('users.sqlite')


#connect to the database
engine = create_engine('sqlite:///users.sqlite')
db = SQLAlchemy()


#class for the table Users
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable = False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    role = db.Column(db.String(80))


Users_tbl = Table('users', Users.metadata)


#fuction to create table using Users class
def create_users_table():
    Users.metadata.create_all(engine)


#create the table
create_users_table()

# If no password was supplied, set it to ''password''

admin_password: str
try:
    admin_password = sys.argv[1]
except IndexError:
    admin_password = "password"
    
print(f"Setting admin password to: {admin_password}")

# # Create the admin user
hashed_password = generate_password_hash(admin_password, method='sha256')
ins = Users_tbl.insert().values(username="admin",  password=hashed_password, email="example@example.com", role="none")
conn = engine.connect()
conn.execute(ins)
conn.close()
