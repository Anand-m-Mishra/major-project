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
<<<<<<< HEAD
    MODEL_PATH = os.path.join(basedir, 'app', 'models', 'mobilenet_model_88.keras')
    CLASS_NAMES = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']  # Update with your class names
    IMAGE_SIZE = (200, 150)  # Should match your model's expected input size
=======
    MODEL_PATH = os.path.join(basedir, 'app', 'models', 'SequentialCNN_DualLayer2_model_66.keras')
    CLASS_NAMES = ['Melanocytic nevi', 'Melanoma', 'Benign keratosis-like lesions', 'Basal cell carcinoma', 'Actinic keratoses', 'Vascular lesions', 'Dermatofibroma', "Normal skin"]  # Example skin lesion classes
    IMAGE_SIZE = (200, 150)  # Adjust based on your model's expected input size
>>>>>>> cfa8a89c7b07f87e1f3ff18a437758336b64ef62
