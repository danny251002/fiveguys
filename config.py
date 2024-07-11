import os

class Config:
    SECRET_KEY = 'sda58was7454' 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True  