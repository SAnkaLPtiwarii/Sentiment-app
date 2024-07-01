from flask import Flask
from flask_socketio import SocketIO, emit
from transformers import pipeline
import re
import logging

from flask_cors import CORS




app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "https://sentiment-em8u4q7z1-sankalptiwariis-projects.vercel.app"}}, 
     supports_credentials=True)

socketio = SocketIO(app, cors_allowed_origins="https://sentiment-em8u4q7z1-sankalptiwariis-projects.vercel.app")


# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load pre-trained sentiment analysis model and emotion detection model
sentiment_analysis = pipeline("sentiment-analysis")
emotion_analysis = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

# Text cleaning function
def clean_text(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'@\w+', '', text)     # Remove mentions
    text is re.sub(r'#\w+', '', text)     # Remove hashtags
    text = re.sub(r'\s+', ' ', text)     # Remove extra spaces
    return text.strip()

@app.route('/')
def index():
    return "Sentiment and Emotion Analysis API is running."

@socketio.on('message')
def handle_message(data):
    app.logger.debug(f"Received message: {data}")
    # Clean the message
    cleaned_message = clean_text(data)
    
    # Perform sentiment analysis
    sentiment_result = sentiment_analysis(cleaned_message)
    app.logger.debug(f"Sentiment analysis result: {sentiment_result}")
    
    # Perform emotion analysis
    emotion_result = emotion_analysis(cleaned_message)
    app.logger.debug(f"Emotion analysis result: {emotion_result}")
    
    # Custom sentiment mapping
    sentiment = sentiment_result[0]['label']
    score = sentiment_result[0]['score']
    
    if sentiment == "POSITIVE" and score < 0.996:
        sentiment = "NEUTRAL"
    elif sentiment == "NEGATIVE" and score < 0.996:
        sentiment = "NEUTRAL"

    # Detailed sentiment scores (if using a model that provides them)
    detailed_scores = {label: score for label, score in sentiment_result[0].items() if label != 'label'}

    # Extract dominant emotion
    dominant_emotion = max(emotion_result[0], key=lambda x: x['score'])

    emit('response', {'message': data, 'sentiment': sentiment, 'score': score, 'details': detailed_scores, 'emotion': dominant_emotion['label']})

if __name__ == '__main__':
    socketio.run(app, debug=True)


