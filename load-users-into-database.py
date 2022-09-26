import sys
import sqlite3
import pandas as pd
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
    username = db.Column(db.String(150), unique=True, nullable = False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(80))
    role = db.Column(db.String(80))


Users_tbl = Table('users', Users.metadata)


# Read the user list
df = pd.read_csv(sys.argv[1])
print("\nLoading these users into the database:\n\n", df, "\n")


# Add each user seperately
for index, row in df.iterrows():
    hashed_password = generate_password_hash(row['password'], method='sha256')
    ins = Users_tbl.insert().values(username=row['username'],  password=hashed_password, email=row['email'], role=row['role'])
    conn = engine.connect()
    conn.execute(ins)
    print(f"Added user: {row['username']}")


conn.close()
