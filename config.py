import os

#  Generate a secure random key
secret_key = os.urandom(32)
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secret_key
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Akanksha%4053@localhost/Hiring_system'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    