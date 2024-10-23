from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import logging
import os
from time import time
from functools import wraps

app = Flask(__name__)

# Configure CORS for production
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, resources={
    r"/*": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize models as None
sentiment_analysis = None
emotion_analysis = None

def init_models():
    
    global sentiment_analysis, emotion_analysis
    try:
        logger.info("Initializing sentiment analysis model...")
        sentiment_analysis = pipeline("sentiment-analysis")
        
        logger.info("Initializing emotion analysis model...")
        emotion_analysis = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            return_all_scores=True
        )
        logger.info("Models initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing models: {str(e)}")
        return False

# Decorator for timing requests
def timer_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        logger.info(f"Request to {f.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

# Decorator to ensure models are loaded
def require_models(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        global sentiment_analysis, emotion_analysis
        if sentiment_analysis is None or emotion_analysis is None:
            if not init_models():
                return jsonify({'error': 'Models not initialized'}), 503
        return f(*args, **kwargs)
    return wrapper

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': sentiment_analysis is not None and emotion_analysis is not None
    })

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'message': "Sentiment Analysis API is running",
        'endpoints': {
            '/analyze': 'POST - Analyze sentiment and emotion',
            '/health': 'GET - Check API health'
        }
    })

@app.route('/analyze', methods=['POST'])
@timer_decorator
@require_models
def analyze():
    """Analyze sentiment and emotion of a message"""
    try:
        # Validate request
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message']
        if not message.strip():
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        logger.info(f"Analyzing message: {message}")
        
        # Perform analysis
        sentiment_result = sentiment_analysis(message)
        emotion_result = emotion_analysis(message)
        
        # Extract results
        sentiment = sentiment_result[0]['label']
        score = sentiment_result[0]['score']
        
        # Get top emotion
        emotions_sorted = sorted(emotion_result[0], key=lambda x: x['score'], reverse=True)
        primary_emotion = emotions_sorted[0]['label']
        
        # Get secondary emotion if score is close
        secondary_emotion = None
        if len(emotions_sorted) > 1:
            if emotions_sorted[1]['score'] > emotions_sorted[0]['score'] * 0.8:  # Within 80% of top score
                secondary_emotion = emotions_sorted[1]['label']
        
        response = {
            'message': message,
            'sentiment': sentiment,
            'score': score,
            'emotion': primary_emotion,
            'secondary_emotion': secondary_emotion,
            'confidence': emotions_sorted[0]['score']
        }
        
        logger.info(f"Analysis complete: {response}")
        return jsonify(response)
        
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    logger.exception("Internal server error")
    return jsonify({'error': 'Internal server error'}), 500

@app.after_request
def after_request(response):
    """Add security headers and CORS headers"""
    # CORS headers
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    
    # Security headers
    response.headers.add('X-Content-Type-Options', 'nosniff')
    response.headers.add('X-Frame-Options', 'DENY')
    response.headers.add('X-XSS-Protection', '1; mode=block')
    response.headers.add('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
    
    return response

if __name__ == '__main__':
    # Initialize models on startup
    init_models()
    
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.environ.get('FLASK_ENV') == 'development'
    )
