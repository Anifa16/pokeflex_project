from app import db, login
from flask_login import UserMixin # Only use UserMixin for the User Model
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

#this is how we declear a table for our resigester users
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #this is how we collect info from user and store it in our database
    first_name = db.Column(db.String, nullable =False) # nullable = false means that we are requiring that input
    last_name = db.Column(db.String, nullable =False)
    email = db.Column(db.String, nullable =False, unique=True) #unique = true means that your email need to be one of kind 
    password = db.Column(db.String, nullable =False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    post=db.relationship('Post', backref='author', lazy='dynamic')

     # hashes our password
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # checks the hashed password
    def check_hash_password(self, login_password):
        return check_password_hash(self.password, login_password)
    
    
    #use the method to rigister to our user attrubets
    def form_dict(self,data):
        self.first_name =data['first_name']
        self.last_name =data['last_name']
        self.email =data['email']
        self.passward = self.hash_password(data['passward'])

    def update_from_dict(self,data):
        self.first_name =data['first_name']
        self.last_name =data['last_name']
        self.email =data['email']

    #save to out database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @login.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    img_url=db.Column(db.String, nullable=False)
    title=db.Column(db.String)
    caption=db.Column(db.String)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign Key to User Table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    # Use this method to register our post attributes
    def form_dict(self, data):
        self.img_url=data['img_url']
        self.title=data['title']
        self.caption=data['caption']
        self.user_id=data['user_id']

    # Save the post to database  
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

        
        
