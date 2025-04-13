from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from .utils import allowed_file, predict_image

bp = Blueprint('main', __name__)

@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Create secure filename
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_filename = f"{timestamp}_{filename}"
            
            # Ensure upload directory exists
            upload_dir = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            # Save file
            save_path = os.path.join(upload_dir, unique_filename)
            file.save(save_path)
            
            # Verify file was saved
            if not os.path.exists(save_path):
                return jsonify({'error': 'File failed to save'}), 500
            
            # Get relative path for frontend
            relative_path = f"/static/uploads/{unique_filename}"
            
            # Make prediction
            prediction = predict_image(save_path)
            
            return jsonify({
                'success': True,
                'filename': relative_path,
                'prediction': prediction
            })
            
        except Exception as e:
            current_app.logger.error(f"Upload error: {str(e)}")
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
    
    return jsonify({'error': 'File type not allowed. Please upload a PNG, JPG, or JPEG image.'}), 400