from app import db,login
from flask_login import UserMixin
from datetime import datetime

#this is how we declear a table for our resigester users
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #this is how we collect info from user and store it in our database
    first_name = db.Column(db.String, nullable =False) # nullable = false means that we are requiring that input
    last_name = db.Column(db.String, nullable =False)
    email = db.Column(db.String, nullable =False, unique=True) #unique = true means that your email need to be one of kind 
    password = db.Column(db.String, nullable =False)
    created_on = db.Column(db.DateTime, defaults = datetime.utcnow)
