import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { useAuth0 } from '@auth0/auth0-react';

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);
  const {getAccessTokenSilently} = useAuth0();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Auto resize textarea height based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'; // reset height
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`; // set new height
    }
  }, [question]);

  const sendMessage = async () => {
  console.log("📡 Sending question:", question);
  if (!question.trim()) return;

  const userMessage = { sender: 'user', text: question };
  setMessages((prev) => [...prev, userMessage]);
  setIsLoading(true);

  try {
    // Call getAccessTokenSilently to get the actual token!
    const token = await getAccessTokenSilently({
      authorizationParams: {
        audience: import.meta.env.VITE_AUTH0_AUDIENCE
      }
    });
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ question }),
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    const data = await res.json();
    console.log("✅ Raw response:", data);

    const botMessage = { sender: 'bot', text: data.response || 'No response.' };
    setMessages((prev) => [...prev, botMessage]);
  } catch (err) {
    console.error("❌ sendMessage error:", err);
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
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault(); // prevent new line
      sendMessage();
    }
  };

  return (
    <div
      style={{
        width: '100%', // Remains responsive
        margin: '20px auto',
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        border: '1px solid #e0e0e0', // Lighter border
        borderRadius: '12px', // More rounded corners
        padding: '1.5rem', // Increased padding
        backgroundColor: '#ffffff', // White background for a cleaner look
        display: 'flex',
        flexDirection: 'column',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.08)', // Subtle shadow
        boxSizing: 'border-box',
      }}
    >
      <h2
        style={{
          marginBottom: '1.5rem',
          textAlign: 'center',
          color: '#333',
          fontSize: '1.8rem', // Larger title
          fontWeight: 600,
        }}
      >
        💬 Ask About Today's News
      </h2>

      <div
        style={{
          flexGrow: 1,
          overflowY: 'auto',
          padding: '1rem',
          border: '1px solid #f0f0f0', // Very light border
          borderRadius: '8px',
          backgroundColor: '#fdfdfd', // Slightly off-white for messages area
          marginBottom: '1.5rem',
          wordBreak: 'break-word',
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem', // Spacing between messages
        }}
      >
        {messages.map((msg, idx) => {
          const isUser = msg.sender === 'user';
          return (
            <div
              key={idx}
              style={{
                display: 'flex',
                justifyContent: isUser ? 'flex-end' : 'flex-start',
              }}
            >
              <div
                style={{
                  maxWidth: '75%', // Slightly wider message bubbles
                  backgroundColor: isUser ? '#007bff' : '#f1f0f0', // Brighter blue for user, soft gray for bot
                  color: isUser ? 'white' : '#333',
                  padding: '12px 18px', // More padding inside bubbles
                  borderRadius: isUser ? '20px 20px 0 20px' : '20px 20px 20px 0', // More pronounced bubble shape
                  fontSize: '1rem',
                  lineHeight: '1.5',
                  boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)', // Subtle shadow for bubbles
                }}
              >
                <strong
                  style={{
                    display: 'block',
                    marginBottom: '6px', // More space below sender name
                    fontSize: '0.9rem',
                    color: isUser ? 'rgba(255, 255, 255, 0.9)' : '#555', // Lighter sender name for user
                  }}
                >
                  {isUser ? 'You' : 'Bot'}
                </strong>
                <ReactMarkdown
                  children={msg.text}
                  components={{
                    a: ({ node, ...props }) => (
                      <a
                        {...props}
                        style={{ color: isUser ? '#a8d8ff' : '#007bff', textDecoration: 'underline' }}
                        target="_blank"
                        rel="noreferrer"
                      />
                    ),
                    code: ({ node, inline, className, children, ...props }) => (
                      <code
                        style={{
                          backgroundColor: '#e9e9e9', // Lighter background for code
                          padding: '3px 6px',
                          borderRadius: '5px',
                          fontFamily: 'monospace',
                          fontSize: '0.9em',
                          color: '#c7254e', // Distinct color for code
                        }}
                        {...props}
                      >
                        {children}
                      </code>
                    ),
                  }}
                />
              </div>
            </div>
          );
        })}
        {isLoading && (
          <div style={{ fontStyle: 'italic', color: '#888', padding: '0 1rem' }}>
            Bot is thinking...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-end' }}>
        <textarea
          ref={textareaRef}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Ask about the articles..."
          rows={1} // Start with 1 row
          style={{
            flexGrow: 1,
            resize: 'none',
            padding: '12px 18px',
            fontSize: '1rem',
            borderRadius: '25px', // More rounded for input
            border: '1px solid #ccc',
            outline: 'none',
            lineHeight: '1.4',
            maxHeight: '150px',
            overflowY: 'auto',
            boxSizing: 'border-box',
            boxShadow: 'inset 0 1px 3px rgba(0, 0, 0, 0.05)', // Inner shadow for depth
            transition: 'border-color 0.2s ease-in-out', // Smooth transition on focus
          }}
          onFocus={(e) => (e.target.style.borderColor = '#007bff')} // Blue border on focus
          onBlur={(e) => (e.target.style.borderColor = '#ccc')} // Revert on blur
          disabled={isLoading}
        />
        <button
          onClick={sendMessage}
          disabled={isLoading || !question.trim()}
          style={{
            padding: '12px 24px',
            backgroundColor: '#007bff', // Brighter blue
            color: 'white',
            border: 'none',
            borderRadius: '25px',
            cursor: isLoading || !question.trim() ? 'not-allowed' : 'pointer',
            fontWeight: 'bold',
            fontSize: '1rem',
            transition: 'background-color 0.2s ease-in-out, transform 0.1s ease-in-out', // Transitions for hover/active
            boxShadow: '0 2px 5px rgba(0, 123, 255, 0.2)', // Subtle shadow
          }}
          onMouseEnter={(e) => !e.currentTarget.disabled && (e.currentTarget.style.backgroundColor = '#0056b3')} // Darker blue on hover
          onMouseLeave={(e) => !e.currentTarget.disabled && (e.currentTarget.style.backgroundColor = '#007bff')} // Revert on leave
          onMouseDown={(e) => !e.currentTarget.disabled && (e.currentTarget.style.transform = 'translateY(1px)')} // Slight press effect
          onMouseUp={(e) => !e.currentTarget.disabled && (e.currentTarget.style.transform = 'translateY(0)')} // Release effect
          aria-label="Send message"
        >
          Send
        </button>
      </div>
    </div>
  );
}