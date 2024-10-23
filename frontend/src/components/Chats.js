import React, { useState } from 'react';
import './Chats.css';

const getEmojiForSentiment = (sentiment) => {
  switch (sentiment.toUpperCase()) {
    case 'POSITIVE':
      return '😊';
    case 'NEGATIVE':
      return '😠';
    case 'NEUTRAL':
      return '😐';
    default:
      return '😐';
  }
};

const getEmojiForEmotion = (emotion) => {
  switch (emotion) {
    case 'joy':
      return '😊';
    case 'anger':
      return '😠';
    case 'sadness':
      return '😢';
    case 'surprise':
      return '😮';
    case 'fear':
      return '😨';
    case 'disgust':
      return '🤢';
    default:
      return '😐';
  }
};

const Chats = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [sentiments, setSentiments] = useState({});
  const [emotions, setEmotions] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeSentiment = async (message) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setSentiments((prev) => ({
        ...prev,
        [message]: {
          sentiment: data.sentiment,
          score: data.score
        },
      }));
      setEmotions((prev) => ({
        ...prev,
        [message]: data.emotion,
      }));
    } catch (error) {
      console.error('Error:', error);
      setError('Failed to analyze message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (message.trim() === '' || isLoading) return;

    setMessages((prev) => [...prev, message]);
    await analyzeSentiment(message);
    setMessage('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chat-container">
      <h1>AI Sentiment Analysis Chat</h1>
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${sentiments[msg]?.sentiment.toLowerCase()}`}>
            <span className="message-text">{msg}</span>
            {sentiments[msg] ? (
              <div className="analysis">
                <span className="emoji">
                  {getEmojiForSentiment(sentiments[msg].sentiment)}
                  <span className="score">
                    Score: {sentiments[msg].score.toFixed(2)}
                  </span>
                </span>
                {emotions[msg] && (
                  <div className="emotion">
                    {getEmojiForEmotion(emotions[msg])} {emotions[msg]}
                  </div>
                )}
              </div>
            ) : (
              <div className="analyzing">
                Analyzing...
              </div>
            )}
          </div>
        ))}
        {error && <div className="error-message">{error}</div>}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message here..."
          disabled={isLoading}
        />
        <button
          onClick={handleSendMessage}
          disabled={message.trim() === '' || isLoading}
        >
          {isLoading ? 'Analyzing...' : 'Send'}
        </button>
      </div>
    </div>
  );
};

export default Chats;