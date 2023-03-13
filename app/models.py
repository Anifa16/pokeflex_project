from app import db, login
from flask_login import UserMixin # Only use UserMixin for the User Model
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash



team = db.Table('team',
        db.Column('pokies_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('pokies_caught', db.Integer, db.ForeignKey('PokemonCaptured.id'))
        )

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('User',
        secondary = followers,
        primaryjoin = (followers.columns.follower_id == id),                     
        secondaryjoin = (followers.columns.followed_id == id),
        backref = db.backref('followers', lazy='dynamic'),
        lazy = 'dynamic'                       
    )
    pokies_caught = db.relationship('PokemonCaptured', secondary = team, backref='pokies', lazy='dynamic')
    
    # hashes our password
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # checks the hashed password
    def check_hash_password(self, login_password):
        return check_password_hash(self.password, login_password)
    
    # Use this method to register our user attributes
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
    
    # Update user attributes
    def update_user(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
    
    # Save the user to database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Update the user to database
    def update_to_db(self):
        db.session.commit()

    # follow user
    def follow_user(self, user):
        self.followed.append(user)
        db.session.commit()
    
    # unfollow user
    def unfollow_user(self, user):
        self.followed.remove(user)
        db.session.commit()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String, nullable=False)
    title = db.Column(db.String)
    caption = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign Key to User Table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Use this method to register our post attributes
    def from_dict(self, data):
        self.img_url = data['img_url']
        self.title = data['title']
        self.caption = data['caption']
        self.user_id = data['user_id']

    # Save the post to database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    # Update the post to databse
    def update_to_db(self):
        db.session.commit()
        
    # Delete the post from database
    def delete_post(self):
        db.session.delete(self)
        db.session.commit()



class PokemonCaptured(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ability = db.Column(db.String)
    base_experience = db.Column(db.Integer)
    sprite_url = db.Column(db.String)
    attack_base_stat = db.Column(db.Integer)
    hp_base_stat = db.Column(db.Integer)
    defense_base_stat = db.Column(db.Integer)
    pokies_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def from_dict(self, data):
        self.name = data['name']
        self.ability = data['ability']
        self.base_experience = data['base_experience']
        self.sprite_url = data['sprite_url']
        self.attack_base_stat = data['attack_base_stat']
        self.hp_base_stat = data['hp_base_stat']
        self.defense_base_stat = data['defense_base_stat']


    # Save the capture to database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Update our db
    def update_to_db(self):
        db.session.commit()

    # Delete from db
    def delete_pokemon(self):
        db.session.delete(self)
        db.session.commit()



