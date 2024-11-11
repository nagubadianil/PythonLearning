import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///employees.db'  # SQLite database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
