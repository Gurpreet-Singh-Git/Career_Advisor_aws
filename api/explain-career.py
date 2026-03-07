from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            career = data.get('career', '')
            user_profile = data.get('user_profile', {})
            score_breakdown = data.get('score_breakdown', {})
            
            # Generate explanation
            explanation = self._generate_explanation(career, user_profile, score_breakdown)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(explanation).encode())
            
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
    
    def _generate_explanation(self, career, profile, breakdown):
        return {
            'career': career,
            'explanation': f"{career} is an excellent match for your profile. Your skills and education align well with the requirements, and there's strong demand in {profile.get('location', 'India')}. This career offers great growth opportunities and competitive salaries.",
            'key_strengths': [
                f"Strong skill alignment ({int(breakdown.get('skill_match', 0)*100)}%)",
                f"Education fits requirements ({int(breakdown.get('education_fit', 0)*100)}%)",
                f"High demand in your region ({int(breakdown.get('regional_demand', 0)*100)}%)"
            ],
            'roadmap': [
                "Step 1: Complete relevant education/certification programs",
                "Step 2: Build practical skills through projects and practice",
                "Step 3: Gain experience through internships or entry-level positions",
                "Step 4: Network with professionals in the field",
                "Step 5: Apply for positions and continue learning"
            ],
            'considerations': "Focus on continuous learning and building a strong portfolio. Consider specializing in high-demand areas within this field.",
            'source': 'demo'
        }
