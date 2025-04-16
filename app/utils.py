import os
import cv2
import numpy as np
from PIL import Image
import joblib
import tensorflow as tf
from config import Config
from keras.models import load_model
from tensorflow.keras.metrics import top_k_categorical_accuracy

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def top_3_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=3)

def top_2_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=2)

def loadModel():
    """Load the .keras model"""
    model = load_model(Config.MODEL_PATH, custom_objects={'top_2_accuracy': top_2_accuracy, 'top_3_accuracy': top_3_accuracy})
    return model

def preprocess_image(image_path, target_size=Config.IMAGE_SIZE):
    """Preprocess the image for your model"""
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    img = img / 255.0  # Normalize
    return np.expand_dims(img, axis=0)

def predict_image(image_path):
    """Make prediction using your model"""
    model = loadModel()
    processed_image = preprocess_image(image_path)
    
    predictions = model.predict(processed_image)
    predicted_class = np.argmax(predictions[0])
    confidence = float(np.max(predictions[0]))
    class_name = Config.CLASS_NAMES[predicted_class]
    print(f"Predicted class: {class_name}, Confidence: {confidence}")
    return {
        'class': class_name,
        'confidence': confidence,
        'all_predictions': predictions.tolist()
    }