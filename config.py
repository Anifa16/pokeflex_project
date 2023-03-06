import os

#my config file
class Config():
    SECRET_KEY=os.environ.get('SECRET_KEY')
    SQLALCHEMY_BASED_URL=os.environ.get('QLALCHEMY_BASED_UR')