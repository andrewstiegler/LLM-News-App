import React, { useState } from 'react';

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!question.trim()) return;

    const userMessage = { sender: 'user', text: question };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();
      const botMessage = { sender: 'bot', text: data.response || 'No response.' };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: '⚠️ Error: Could not get response.' },
      ]);
    } finally {
      setIsLoading(false);
      setQuestion('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  return (
    <div className="chat-box">
      <h2>💬 Ask About Today's News</h2>
      <div className="chat-messages" style={{ maxHeight: '300px', overflowY: 'auto', marginBottom: '1rem' }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left' }}>
            <strong>{msg.sender === 'user' ? 'You' : 'Bot'}:</strong> {msg.text}
          </div>
        ))}
        {isLoading && <div><em>Bot is thinking...</em></div>}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Ask about the articles..."
          style={{ width: '80%', marginRight: '1rem' }}
        />
        <button onClick={sendMessage} disabled={isLoading}>Send</button>
      </div>
    </div>
  );
}
