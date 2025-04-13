import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('1234') or '1234'
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    TEMPLATES_FOLDER = os.path.join(basedir, 'app', 'templates') 
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    
    # Model configuration
    MODEL_PATH = os.path.join(basedir, 'app', 'models', 'model.pkl')
    CLASS_NAMES = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']  # Example skin lesion classes
    IMAGE_SIZE = (224, 224)  # Adjust based on your model's expected input size