from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            message = data.get('message', '')
            
            # Fallback AI response (works without AWS)
            response = self._get_ai_response(message)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _get_ai_response(self, message):
        message_lower = message.lower()
        
        # Check for personalized recommendation request
        if any(word in message_lower for word in ['recommend', 'personalized', 'for me', 'help me choose']):
            return {
                'response': "I'd be happy to provide personalized career recommendations! To give you the best suggestions based on your unique profile, I'll need to know about your education, skills, interests, and location. Would you like to fill out a quick form to get your top 3 career matches?",
                'source': 'demo',
                'requires_form': True
            }
        
        # Check for BTech/career questions
        elif any(word in message_lower for word in ['btech', 'worth', 'should i']):
            return {
                'response': "That's a great question! The value of pursuing B.Tech in 2026 depends on several factors:\n\n1. Strong Demand: Technology careers remain in high demand in India, especially in cities like Bangalore, Hyderabad, and Pune. Software engineers and data scientists continue to have excellent job prospects.\n\n2. Evolving Skills: While a B.Tech degree provides a strong foundation, the tech industry values practical skills and continuous learning. Focus on building projects, learning in-demand technologies, and gaining internship experience.\n\n3. Consider Your Interests: B.Tech is worth it if you're genuinely interested in technology and problem-solving. If you'd like personalized career recommendations based on your specific interests and skills, I can help with that!",
                'source': 'demo',
                'requires_form': False
            }
        
        # General career exploration
        else:
            return {
                'response': "I'm here to help you with career guidance! I can:\n\n• Answer questions about specific careers\n• Explain education paths and requirements\n• Discuss job market trends in India\n• Provide personalized career recommendations\n\nWhat would you like to know about careers?",
                'source': 'demo',
                'requires_form': False
            }
