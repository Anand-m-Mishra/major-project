import os
import cv2
import numpy as np
from PIL import Image
import joblib
from config import Config

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def load_model():
    """Load the .pkl model"""
    return joblib.load(Config.MODEL_PATH)

def preprocess_image(image_path, target_size=Config.IMAGE_SIZE):
    """Preprocess the image for your model"""
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    img = img / 255.0  # Normalize
    return np.expand_dims(img, axis=0)

def predict_image(image_path):
    """Make prediction using your model"""
    model = load_model()
    processed_image = preprocess_image(image_path)
    
    predictions = model.predict(processed_image)
    predicted_class = np.argmax(predictions[0])
    confidence = float(np.max(predictions[0]))
    class_name = Config.CLASS_NAMES[predicted_class]
    
    return {
        'class': class_name,
        'confidence': confidence,
        'all_predictions': predictions.tolist()
    }