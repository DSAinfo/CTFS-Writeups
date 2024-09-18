class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../config.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'fake_secret_key_value'