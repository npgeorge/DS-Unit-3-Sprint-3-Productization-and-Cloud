from flask_sqlalchemy import SQLAlchemy

#Minimum viable model with some base code

#all DB. calls are from SQLAlchemy
DB = SQLAlchemy()

class User(DB.Model):
    """ Twitter users that we pull and analyze tweets for """
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False) #you are not allowed to have a null name

class Tweet(DB.Model):
    """Tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(280))