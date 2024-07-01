
# Real-Time Sentiment Analysis Chat Application

This project is a real-time chat application that integrates sentiment analysis. As users type messages, the app analyzes the sentiment and provides instant feedback with emojis representing the sentiment score.

## Features

- Real-time chat functionality
- Sentiment analysis using a pre-trained model from Hugging Face
- Instant feedback with emojis based on sentiment
- Prevents sending of empty messages

## Tech Stack

- **Frontend**: React
- **Backend**: Flask
- **Sentiment Analysis**: Hugging Face's `transformers` library
- **WebSocket**: `flask-socketio`

## Setup and Installation

### Prerequisites

- [Node.js](https://nodejs.org/en/download/)
- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

### Installation Steps

1. **Clone the repository**:

    ```bash
    git clone git@github.com:SAnKaLPtiwarii/sentiment-analysis-chat-app.git
    cd sentiment-analysis-chat-app
    ```

2. **Backend Setup**:

    - Navigate to the backend directory:

        ```bash
        cd backend
        ```

    - Create a virtual environment and activate it:

        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
        ```

    - Install the required packages:

        ```bash
        pip install -r requirements.txt
        ```

3. **Frontend Setup**:

    - Navigate to the frontend directory:

        ```bash
        cd ../frontend
        ```

    - Install the required packages:

        ```bash
        npm install
        ```

### Running the Application

1. **Start the backend server**:

    - Navigate to the backend directory:

        ```bash
        cd backend
        ```

    - Run the Flask server:

        ```bash
        flask run
        ```

    - The backend will be running at `http://127.0.0.1:5000`.

2. **Start the frontend server**:

    - Navigate to the frontend directory:

        ```bash
        cd ../frontend
        ```

    - Run the React development server:

        ```bash
        npm start
        ```

    - The frontend will be running at `http://127.0.0.1:3000`.

## Usage

- Open the application in your browser: `http://127.0.0.1:3000`
- Type a message in the chat input box.
- The application will display an emoji representing the sentiment of your message in real-time.

## Project Structure

```plaintext
sentiment-analysis-chat-app/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── venv/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat.js
│   │   │   ├── MessageList.js
│   │   │   ├── MessageInput.js
│   │   │   └── Emoji.js
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   └── package-lock.json
└── README.md
