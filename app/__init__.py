from flask import Flask
from .routes import v0_blueprint, initialize_limiter , get_client_ip   # Import blueprints
from flask_limiter import Limiter

def create_app(config_name=None):
    app = Flask(__name__)

    # Load configuration
    if config_name:
        app.config.from_object(config_name)
    
    # Initialize the Limiter with default settings
    limiter = Limiter(
        key_func=get_client_ip,
        app=app,
        default_limits=["30 per minute"]
    )

    # Initialize limiter in routes
    initialize_limiter(limiter)

    # Register blueprints
    app.register_blueprint(v0_blueprint, url_prefix='/v0')
    return app
