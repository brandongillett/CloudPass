##API ADDRESS####
API_ADDRESS = 'http://fastapi:8000'
#######################

##Encryption method####
encryptMethod = 'sha256'
#######################

class Config:
    DEBUG = True
    SECRET_KEY = 'CloudPass'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PERMANENT_SESSION_LIFETIME = 600