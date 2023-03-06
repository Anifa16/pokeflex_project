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
    created_on = db.Column(db.DateTime, default=datetime.utcnow())

#hash our passward
def hash_password(self, original_password):
    return generate_password_has(original_password)

#check password#
def check_hash_password(self, login_password):
    return check_oassword_password_hash(self.password, login_password)

#use the method to rigister to our user attrubets
def form_dict(self,data):
    self.first_name =data['first_name']
    self.last_name =data['last_name']
    self.email =data['email']
    self.passward = self.hash_password(data['passward'])

#save to out database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)