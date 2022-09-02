# create models here
import pandas as pd
#Needed the db for creating and binding model class
#Ideally the db wouldnt be instantianted in the init file as importing from that file can be problematic 
from app import db
#Data Results
df = pd.read_excel('DataResults.xlsx')
#Trades Model
#Id column auto populates and increments when new trade instance is created
class Trades(db.Model):
  __tablename__ = "trades"
  id = db.Column(db.Integer, primary_key=True,autoincrement=True)
  trade_type = db.Column(db.String)
  user_id = db.Column(db.Integer)
  symbol = db.Column(db.String)
  shares = db.Column(db.Integer)
  price = db.Column(db.Integer)
  timestamp = db.Column(db.Integer)
