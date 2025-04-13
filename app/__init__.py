from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates')  # Add template_folder here
    app.config.from_object(config_class)

    # Ensure upload folder exists
    import os
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Register blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app