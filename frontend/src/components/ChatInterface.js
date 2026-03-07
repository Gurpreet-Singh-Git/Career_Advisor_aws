import React, { useState } from 'react';

function ChatInterface({ onSubmit }) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      onSubmit(message);
      setMessage('');
    }
  };

  const quickOptions = [
    "I want personalized career recommendations",
    "Explore career options in technology",
    "What careers are good for science students?"
  ];

  return (
    <div className="chat-interface">
      <div className="chat-welcome">
        <h2>Welcome! How can I help you today?</h2>
        <p>You can ask me about careers, or get personalized recommendations.</p>
      </div>

      <div className="quick-options">
        <p>Quick options:</p>
        {quickOptions.map((option, index) => (
          <button 
            key={index}
            className="quick-option-btn"
            onClick={() => onSubmit(option)}
          >
            {option}
          </button>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="chat-form">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message here..."
          className="chat-input"
        />
        <button type="submit" className="chat-submit">Send</button>
      </form>
    </div>
  );
}

export default ChatInterface;
