import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('1234') or '1234'
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    
    # Model configuration
    MODEL_PATH = os.path.join(basedir, 'app', 'models', 'mobilenet_model_88.keras')
    CLASS_NAMES = ['Melanocytic nevi', 'Melanoma', 'Benign keratosis-like lesions', 'Basal cell carcinoma', 'Actinic keratoses', 'Vascular lesions', 'Dermatofibroma', "Normal skin"]  # Example skin lesion classes
    IMAGE_SIZE = (200, 150)  # Adjust based on your model's expected input size
