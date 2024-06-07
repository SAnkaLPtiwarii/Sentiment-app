import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import './Chats.css';

const socket = io('http://localhost:5000');

const getEmojiForSentiment = (sentiment) => {
  switch (sentiment) {
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

  useEffect(() => {
    socket.on('response', (data) => {
      setSentiments((prev) => ({
        ...prev,
        [data.message]: { sentiment: data.sentiment, score: data.score, details: data.details },
      }));
      setEmotions((prev) => ({
        ...prev,
        [data.message]: data.emotion,
      }));
    });
  }, []);

  const handleSendMessage = () => {
    socket.send(message);
    setMessages((prev) => [...prev, message]);
    setMessage('');
  };

  return (
    <div className="chat-container">
      <h1>Real-time Sentiment and Emotion Analysis Chat</h1>
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${sentiments[msg]?.sentiment.toLowerCase()}`}>
            <span>{msg}</span>
            {sentiments[msg] && (
              <span className="emoji">
                {getEmojiForSentiment(sentiments[msg].sentiment)} ({sentiments[msg].score.toFixed(2)})
                <div className="details">
                  {Object.entries(sentiments[msg].details).map(([label, score]) => (
                    <div key={label}>{label}: {score.toFixed(2)}</div>
                  ))}
                </div>
                <div className="emotion">
                  Emotion: {getEmojiForEmotion(emotions[msg])} {emotions[msg]}
                </div>
              </span>
            )}
          </div>
        ))}
      </div>
      <input
        type="text"
        id="message-input"
        name="message"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type a message"
      />
      <button onClick={handleSendMessage} disabled={message.trim() === ''}>Send</button>
    </div>
  );
};

export default Chats;

