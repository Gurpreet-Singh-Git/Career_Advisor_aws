"""
Local Flask server for testing Career Guidance System
Run this to test the system without AWS
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
sys.path.append('backend')

from ai_chat.bedrock_chat import BedrockChat
from career_ranking.ranker import CareerRanker

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize modules
bedrock_chat = BedrockChat()
career_ranker = CareerRanker()

# Store conversation history per session (in production, use DynamoDB)
conversations = {}

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Career Guidance API is running'})

@app.route('/api/chat', methods=['POST'])
def chat():
    """AI-powered chat endpoint using AWS Bedrock"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get conversation history
        history = conversations.get(session_id, [])
        
        # Get AI response
        result = bedrock_chat.chat(message, history)
        
        # Update conversation history
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": result['response']})
        conversations[session_id] = history[-10:]  # Keep last 10 messages
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/detect-intent', methods=['POST'])
def detect_intent():
    """Legacy endpoint - redirects to chat"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Use AI chat instead of rule-based detection
        result = bedrock_chat.chat(message)
        
        return jsonify({
            'intent': 'personalized_guidance' if result.get('requires_form') else 'exploration',
            'requires_consent': result.get('requires_form', False),
            'message': result['response'],
            'consent_prompt': "To provide personalized career recommendations, I'll need to ask about your education, skills, interests, and location. This information will only be used for this session and won't be permanently stored. Do you consent to proceed?",
            'original_query': message,
            'ai_powered': True,
            'source': result.get('source', 'unknown')
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rank-careers', methods=['POST'])
def rank_careers():
    """Rank careers based on user profile"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['education', 'skills', 'interests', 'location']
        if not all(field in data for field in required):
            return jsonify({'error': f'Missing required fields: {required}'}), 400
        
        # Rank careers
        rankings = career_ranker.rank(
            education=data['education'],
            skills=data['skills'],
            interests=data['interests'],
            location=data['location']
        )
        
        return jsonify({'careers': rankings})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/explain-career', methods=['POST'])
def explain_career():
    """Generate explanation for career recommendation using AWS Bedrock"""
    try:
        data = request.get_json()
        
        required = ['career', 'user_profile', 'score_breakdown']
        if not all(field in data for field in required):
            return jsonify({'error': f'Missing required fields: {required}'}), 400
        
        career = data['career']
        profile = data['user_profile']
        breakdown = data['score_breakdown']
        
        # Build prompt for Bedrock
        prompt = f"""Explain why {career} is a good match for this student profile:

Education: {profile['education']}
Skills: {', '.join(profile['skills'])}
Interests: {', '.join(profile['interests'])}
Location: {profile['location']}

ML Scoring Breakdown:
- Skill Match: {int(breakdown['skill_match']*100)}%
- Education Fit: {int(breakdown['education_fit']*100)}%
- Interest Alignment: {int(breakdown['interest_alignment']*100)}%
- Regional Demand: {int(breakdown['regional_demand']*100)}%

Provide:
1. A brief explanation (2-3 sentences) of why this career matches
2. 3 key strengths
3. A 5-step roadmap specific to India
4. Important considerations

Keep it concise and actionable."""
        
        # Get AI explanation
        result = bedrock_chat.chat(prompt)
        
        # Parse response (in production, use structured output)
        explanation = {
            'career': career,
            'explanation': result['response'],
            'key_strengths': [
                f"Strong skill alignment ({int(breakdown['skill_match']*100)}%)",
                f"Education fits requirements ({int(breakdown['education_fit']*100)}%)",
                f"High demand in your region ({int(breakdown['regional_demand']*100)}%)"
            ],
            'roadmap': [
                "Step 1: Complete relevant education/certification programs",
                "Step 2: Build practical skills through projects",
                "Step 3: Gain experience through internships",
                "Step 4: Network with professionals in the field",
                "Step 5: Apply for positions and continue learning"
            ],
            'considerations': "Focus on continuous learning and building a strong portfolio.",
            'source': result.get('source', 'unknown')
        }
        
        return jsonify(explanation)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  🚀 AI CAREER GUIDANCE SYSTEM - LOCAL SERVER")
    print("="*70)
    print("\n  Server starting on http://localhost:5000")
    print("\n  Available endpoints:")
    print("    GET  /api/health")
    print("    POST /api/chat                (NEW: AI-powered chat)")
    print("    POST /api/detect-intent       (Legacy: uses AI now)")
    print("    POST /api/rank-careers")
    print("    POST /api/explain-career      (Uses AWS Bedrock)")
    print("\n  AI Features:")
    print("    ✓ Dynamic conversations with AWS Bedrock")
    print("    ✓ Natural language understanding")
    print("    ✓ Context-aware responses")
    print("    ✓ Fallback mode when AWS not configured")
    print("\n  Next steps:")
    print("    1. Keep this server running")
    print("    2. Open a new terminal")
    print("    3. Run: cd frontend && npm start")
    print("\n" + "="*70 + "\n")
    
    app.run(debug=True, port=5000)
