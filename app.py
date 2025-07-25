import os
import logging
from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Enable CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize ML model on startup
from models.forecast_model import ForecastModel
forecast_model = ForecastModel()

# Register blueprints
from api.routes import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

# Main routes
from flask import render_template

@app.route('/')
def index():
    """Home page with API overview"""
    return render_template('index.html')

@app.route('/docs')
def documentation():
    """API documentation page"""
    return render_template('documentation.html')

@app.errorhandler(404)
def not_found(error):
    return {"error": "Endpoint not found", "status": 404}, 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return {"error": "Internal server error", "status": 500}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
