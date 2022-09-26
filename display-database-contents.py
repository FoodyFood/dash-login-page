import pandas as pd
import sqlite3
from sqlalchemy import Table, create_engine
from flask_sqlalchemy import SQLAlchemy


conn = sqlite3.connect('users.sqlite')

c = conn.cursor()
df = pd.read_sql('select * from users', conn)
print(df)