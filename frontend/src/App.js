import React, { useState } from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';
import CareerForm from './components/CareerForm';
import ResultsDisplay from './components/ResultsDisplay';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

// Demo mode flag - set to true for presentation
const DEMO_MODE = true;

function App() {
  const [mode, setMode] = useState('chat'); // 'chat', 'form', 'results'
  const [careerResults, setCareerResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleIntentDetection = async (message) => {
    setLoading(true);
    
    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    try {
      if (DEMO_MODE) {
        // Static demo responses
        const lowerMessage = message.toLowerCase();
        let response = '';
        let requiresForm = false;
        
        if (lowerMessage.includes('personalized') || lowerMessage.includes('recommendation')) {
          response = "I'd be happy to provide personalized career recommendations! To give you the best suggestions, I'll need to understand your background, skills, and interests. Would you like to proceed?";
          requiresForm = true;
        } else if (lowerMessage.includes('btech') || lowerMessage.includes('engineering')) {
          response = "BTech remains a strong choice in 2026! With India's growing tech sector, engineering graduates have excellent opportunities in software development, AI/ML, and emerging technologies. The average starting salary ranges from ₹4-8 lakhs, with top companies offering ₹15+ lakhs. Would you like personalized recommendations based on your profile?";
          requiresForm = false;
        } else if (lowerMessage.includes('career') || lowerMessage.includes('job')) {
          response = "India offers diverse career opportunities across technology, healthcare, finance, and creative fields. Popular careers include Software Engineer, Data Scientist, Digital Marketing, and Healthcare professionals. Each has unique requirements and growth potential. Would you like personalized recommendations?";
          requiresForm = false;
        } else {
          response = "I'm here to help you explore career options! You can ask about specific careers, education paths, or get personalized recommendations based on your skills and interests. What would you like to know?";
          requiresForm = false;
        }
        
        // Show AI response
        alert(`AI: ${response}\n\n✨ Powered by AWS Bedrock (Demo Mode)`);
        
        if (requiresForm) {
          const consent = window.confirm(
            "To provide personalized career recommendations, I'll need to ask about your education, skills, interests, and location. This information will only be used for this session. Do you consent to proceed?"
          );
          if (consent) {
            setMode('form');
          }
        }
      } else {
        // Original API call code
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
        alert(`AI: ${data.response}\n\n${data.source === 'bedrock' ? '✨ Powered by AWS Bedrock' : '💡 Fallback mode'}`);
        
        if (data.requires_form) {
          const consent = window.confirm(
            "To provide personalized career recommendations, I'll need to ask about your education, skills, interests, and location. This information will only be used for this session. Do you consent to proceed?"
          );
          if (consent) {
            setMode('form');
          }
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
    
    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    try {
      if (DEMO_MODE) {
        // Static demo data based on form input
        const demoRankings = [
          {
            title: "Software Engineer",
            score: 87,
            breakdown: {
              skill_match: 90,
              education_fit: 85,
              interest_alignment: 88,
              regional_demand: 85
            }
          },
          {
            title: "Data Scientist",
            score: 82,
            breakdown: {
              skill_match: 85,
              education_fit: 80,
              interest_alignment: 82,
              regional_demand: 80
            }
          },
          {
            title: "Cloud Solutions Architect",
            score: 78,
            breakdown: {
              skill_match: 80,
              education_fit: 75,
              interest_alignment: 80,
              regional_demand: 78
            }
          }
        ];
        
        const demoExplanations = [
          {
            explanation: `Software Engineering is an excellent match for you! With your ${formData.education_level} background and skills in ${formData.skills.slice(0, 2).join(' and ')}, you're well-positioned for this career.\n\nWhy this fits you:\nYour strong technical skills and interest in ${formData.interests[0]} align perfectly with software development. The Indian tech industry is booming, especially in ${formData.location}, with companies actively hiring.\n\nYour Roadmap:\n1. Master data structures and algorithms\n2. Build 3-5 portfolio projects\n3. Contribute to open-source projects\n4. Apply to product-based companies\n\nStarting salary: ₹6-12 lakhs, growing to ₹20+ lakhs with experience. You've got this! 🚀`
          },
          {
            explanation: `Data Science is a fantastic career path for you! Your analytical mindset and ${formData.education_level} education provide a solid foundation.\n\nWhy this fits you:\nYour interest in ${formData.interests[1] || formData.interests[0]} and technical skills make you ideal for data-driven roles. ${formData.location} has a growing demand for data professionals.\n\nYour Roadmap:\n1. Learn Python, SQL, and statistics\n2. Master ML libraries (scikit-learn, TensorFlow)\n3. Complete 2-3 data analysis projects\n4. Build a portfolio on GitHub/Kaggle\n\nStarting salary: ₹5-10 lakhs, reaching ₹25+ lakhs as you gain expertise. The future is data-driven! 📊`
          },
          {
            explanation: `Cloud Solutions Architect is an emerging and lucrative career! Your technical background positions you well for this role.\n\nWhy this fits you:\nWith your ${formData.education_level} and interest in ${formData.interests[0]}, you can excel in cloud technologies. ${formData.location} has increasing demand for cloud experts.\n\nYour Roadmap:\n1. Get AWS/Azure/GCP certifications\n2. Learn infrastructure as code (Terraform)\n3. Build cloud-based projects\n4. Gain experience with microservices\n\nStarting salary: ₹7-14 lakhs, growing to ₹30+ lakhs with certifications and experience. Cloud is the future! ☁️`
          }
        ];
        
        setCareerResults({
          rankings: demoRankings,
          explanations: demoExplanations
        });
        setMode('results');
      } else {
        // Original API call code
        const rankResponse = await fetch(`${API_BASE_URL}/api/rank-careers`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        });
        const rankings = await rankResponse.json();

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
      }
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
