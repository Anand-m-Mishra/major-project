from flask import Blueprint, request, jsonify, send_from_directory, current_app, render_template
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from .utils import allowed_file, predict_image

bp = Blueprint('main', __name__)

# Serve the main SPA template for all routes
@bp.route('/', methods=['GET'])
@bp.route('/home', methods=['GET'])
@bp.route('/results', methods=['GET'])
@bp.route('/history', methods=['GET'])
def index():
    return render_template('index.html')

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
                'prediction': prediction,
                'redirect': '/results'  # Tell frontend to navigate to results
            })
            
        except Exception as e:
            current_app.logger.error(f"Upload error: {str(e)}")
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
    
    return jsonify({'error': 'File type not allowed. Please upload a PNG, JPG, or JPEG image.'}), 400

@bp.route('/api/results', methods=['GET'])
def get_results_data():
    """API endpoint to fetch results data"""
    # In a real app, you would query your database here
    # This is just a placeholder response
    return jsonify({
        'recent_results': [
            {
                'id': 'DS-2023-08-25-42X7',
                'image_url': '/static/uploads/sample1.jpg',
                'diagnosis': 'melanoma',
                'confidence': 87,
                'date': '2023-08-25'
            }
        ]
    })

@bp.route('/api/history', methods=['GET'])
def get_history_data():
    """API endpoint to fetch history data"""
    # In a real app, you would query your database here
    # This is mock data for demonstration
    return jsonify([
        {
            'id': 'DS-2023-08-25-42X7',
            'image_url': '/static/uploads/sample1.jpg',
            'diagnosis': 'melanoma',
            'confidence': 87,
            'date': '2023-08-25'
        },
        {
            'id': 'DS-2023-08-20-39B2',
            'image_url': '/static/uploads/sample2.jpg',
            'diagnosis': 'nevus',
            'confidence': 92,
            'date': '2023-08-20'
        }
    ])

@bp.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)