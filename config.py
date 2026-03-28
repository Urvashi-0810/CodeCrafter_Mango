import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    FLASK_ENV = "production"
    GEMINI_MODEL = "gemini-pro"
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = "development"

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": Config,
    "default": DevelopmentConfig
}

FLASK_ENV = os.getenv("FLASK_ENV", "development")
