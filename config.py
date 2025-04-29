import os

#  Generate a secure random key
secret_key = os.urandom(32)
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secret_key
    SQLALCHEMY_DATABASE_URI =  os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    