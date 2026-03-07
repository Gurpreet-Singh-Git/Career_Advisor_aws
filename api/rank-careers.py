from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Get user profile
            education = data.get('education', '')
            skills = data.get('skills', [])
            interests = data.get('interests', [])
            location = data.get('location', '')
            
            # Simple ranking logic
            careers = self._rank_careers(education, skills, interests, location)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {'careers': careers}
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
    
    def _rank_careers(self, education, skills, interests, location):
        # Sample careers with scoring
        all_careers = [
            {
                'title': 'Software Engineer',
                'category': 'Technology',
                'required_skills': ['python', 'java', 'programming'],
                'interests': ['technology', 'coding'],
                'education': ['btech', 'bsc'],
                'salary_range': '₹4-15 LPA',
                'growth_outlook': 'Excellent'
            },
            {
                'title': 'Data Scientist',
                'category': 'Technology',
                'required_skills': ['python', 'statistics', 'machine learning'],
                'interests': ['data', 'analysis', 'technology'],
                'education': ['btech', 'mtech', 'msc'],
                'salary_range': '₹6-20 LPA',
                'growth_outlook': 'Excellent'
            },
            {
                'title': 'Business Analyst',
                'category': 'Business',
                'required_skills': ['analysis', 'excel', 'communication'],
                'interests': ['business', 'analysis'],
                'education': ['btech', 'bcom', 'mba'],
                'salary_range': '₹5-15 LPA',
                'growth_outlook': 'Very Good'
            }
        ]
        
        scored_careers = []
        for career in all_careers:
            score = self._calculate_score(career, skills, interests, education, location)
            scored_careers.append({
                'title': career['title'],
                'category': career['category'],
                'score': score,
                'breakdown': {
                    'skill_match': min(score + 0.1, 1.0),
                    'education_fit': 1.0 if education.lower() in [e.lower() for e in career['education']] else 0.7,
                    'interest_alignment': min(score, 1.0),
                    'regional_demand': 0.85
                },
                'metadata': {
                    'avg_salary_range': career['salary_range'],
                    'growth_outlook': career['growth_outlook'],
                    'education_required': '/'.join(career['education'])
                }
            })
        
        # Sort by score and return top 3
        scored_careers.sort(key=lambda x: x['score'], reverse=True)
        return scored_careers[:3]
    
    def _calculate_score(self, career, user_skills, user_interests, education, location):
        score = 0.5  # Base score
        
        # Skill match
        user_skills_lower = [s.lower() for s in user_skills]
        career_skills_lower = [s.lower() for s in career['required_skills']]
        skill_matches = len(set(user_skills_lower) & set(career_skills_lower))
        if skill_matches > 0:
            score += 0.2
        
        # Interest match
        user_interests_lower = [i.lower() for i in user_interests]
        career_interests_lower = [i.lower() for i in career['interests']]
        interest_matches = len(set(user_interests_lower) & set(career_interests_lower))
        if interest_matches > 0:
            score += 0.2
        
        # Education match
        if education.lower() in [e.lower() for e in career['education']]:
            score += 0.1
        
        return min(score, 1.0)
