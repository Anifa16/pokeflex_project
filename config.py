import os

#my config file
class Config():
    SECRET_KEY=os.environ.get('SECRET_KEY')
    REGISTER_USER={
        'ann@gmail.com':{
            'name': 'ann'
            'password':'test124'
        }
    }
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')