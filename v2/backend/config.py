import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/typetrain'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'some_secret_here'  # Used for securely signing the session cookie
    JWT_ALGORITHM = 'HS256'  # Algorithm used for encoding and decoding JWT tokens
