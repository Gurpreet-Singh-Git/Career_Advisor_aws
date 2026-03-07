import React, { useState } from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';
import CareerForm from './components/CareerForm';
import ResultsDisplay from './components/ResultsDisplay';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

function App() {
  const [mode, setMode] = useState('chat'); // 'chat', 'form', 'results'
  const [userConsent, setUserConsent] = useState(false);
  const [careerResults, setCareerResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleIntentDetection = async (message) => {
    setLoading(true);
    try {
      console.log('Sending AI chat request:', message);
      console.log('API URL:', API_BASE_URL);
      
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message,
          session_id: 'user_session_' + Date.now()
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('AI response:', data);
      
      // Show AI response
      alert(`AI: ${data.response}\n\n${data.source === 'bedrock' ? '✨ Powered by AWS Bedrock' : '💡 Fallback mode'}`);
      
      if (data.requires_form) {
        // Show consent prompt
        console.log('AI suggests filling form');
        const consent = window.confirm(
          "To provide personalized career recommendations, I'll need to ask about your education, skills, interests, and location. This information will only be used for this session. Do you consent to proceed?"
        );
        console.log('User consent:', consent);
        setUserConsent(consent);
        if (consent) {
          setMode('form');
        }
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to process request. Please try again. Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFormSubmit = async (formData) => {
    setLoading(true);
    try {
      // Get career rankings
      const rankResponse = await fetch(`${API_BASE_URL}/api/rank-careers`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const rankings = await rankResponse.json();

      // Get explanations for top careers
      const explanations = await Promise.all(
        rankings.careers.map(async (career) => {
          const explainResponse = await fetch(`${API_BASE_URL}/api/explain-career`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              career: career.title,
              user_profile: formData,
              score_breakdown: career.breakdown
            })
          });
          return explainResponse.json();
        })
      );

      setCareerResults({
        rankings: rankings.careers,
        explanations
      });
      setMode('results');
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to get recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎓 AI Career Guidance for Indian Students</h1>
        <p>Discover your ideal career path with AI-powered recommendations</p>
      </header>

      <main className="App-main">
        {loading && <div className="loading">Processing...</div>}
        
        {mode === 'chat' && !loading && (
          <ChatInterface onSubmit={handleIntentDetection} />
        )}
        
        {mode === 'form' && !loading && (
          <CareerForm onSubmit={handleFormSubmit} onBack={() => setMode('chat')} />
        )}
        
        {mode === 'results' && !loading && careerResults && (
          <ResultsDisplay 
            results={careerResults} 
            onStartOver={() => {
              setMode('chat');
              setUserConsent(false);
              setCareerResults(null);
            }}
          />
        )}
      </main>

      <footer className="App-footer">
        <p>🔒 Your data is used only for this session and not permanently stored</p>
        <p>⚠️ These are recommendations, not guarantees. Make informed decisions.</p>
      </footer>
    </div>
  );
}

export default App;
