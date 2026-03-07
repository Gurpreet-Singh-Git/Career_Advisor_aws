"""
LLM Explanation Layer
Uses AWS Bedrock to generate career explanations and roadmaps
LLM is used ONLY for explanation, NOT for decision-making
"""
import json
import boto3
from typing import Dict

class CareerExplainer:
    """Generates explanations using AWS Bedrock (Claude/Titan)"""
    
    def __init__(self):
        self.bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
    
    def explain(self, career: str, user_profile: Dict, score_breakdown: Dict) -> Dict:
        """
        Generate explanation for career recommendation
        
        Args:
            career: Career title
            user_profile: User's education, skills, interests, location
            score_breakdown: Scoring breakdown from ranking engine
            
        Returns:
            Dict with explanation and roadmap
        """
        # Build prompt with strict constraints
        prompt = self._build_prompt(career, user_profile, score_breakdown)
        
        # Call Bedrock
        response = self._call_bedrock(prompt)
        
        # Parse and structure response
        return self._parse_response(response, career)
    
    def _build_prompt(self, career: str, user_profile: Dict, score_breakdown: Dict) -> str:
        """Build structured prompt for Bedrock"""
        
        prompt_template = f"""You are a career guidance assistant for Indian students. Your role is to EXPLAIN career recommendations, not make decisions.

IMPORTANT CONSTRAINTS:
- You are explaining a career that has ALREADY been ranked by an ML system
- Do NOT suggest alternative careers or question the ranking
- Focus ONLY on explaining WHY this career fits the user
- Be specific to the Indian education system and job market
- Keep explanations concise (150-200 words)
- Provide actionable roadmap steps

CAREER TO EXPLAIN: {career}

USER PROFILE:
- Education: {user_profile.get('education', 'Not specified')}
- Skills: {', '.join(user_profile.get('skills', []))}
- Interests: {', '.join(user_profile.get('interests', []))}
- Location: {user_profile.get('location', 'India')}

ML SCORING BREAKDOWN (0.0 to 1.0):
- Skill Match: {score_breakdown.get('skill_match', 0.0)} (35% weight)
- Education Fit: {score_breakdown.get('education_fit', 0.0)} (25% weight)
- Interest Alignment: {score_breakdown.get('interest_alignment', 0.0)} (25% weight)
- Regional Demand: {score_breakdown.get('regional_demand', 0.0)} (15% weight)

TASK:
1. Explain WHY this career matches the user's profile based on the scores above
2. Highlight specific connections between user's skills/interests and career requirements
3. Provide a 5-step roadmap specific to Indian context (education, certifications, experience)

FORMAT YOUR RESPONSE AS JSON:
{{
  "explanation": "Your explanation here...",
  "key_strengths": ["strength 1", "strength 2", "strength 3"],
  "roadmap": [
    "Step 1: ...",
    "Step 2: ...",
    "Step 3: ...",
    "Step 4: ...",
    "Step 5: ..."
  ],
  "considerations": "Any important considerations or challenges..."
}}

Generate the JSON response now:"""
        
        return prompt_template
    
    def _call_bedrock(self, prompt: str) -> str:
        """Call AWS Bedrock API"""
        try:
            # Prepare request for Claude
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            # Invoke model
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            # Fallback to template-based explanation
            return self._fallback_explanation()
    
    def _parse_response(self, response: str, career: str) -> Dict:
        """Parse LLM response into structured format"""
        try:
            # Try to parse JSON response
            parsed = json.loads(response)
            return {
                'career': career,
                'explanation': parsed.get('explanation', ''),
                'key_strengths': parsed.get('key_strengths', []),
                'roadmap': parsed.get('roadmap', []),
                'considerations': parsed.get('considerations', ''),
                'source': 'bedrock'
            }
        except json.JSONDecodeError:
            # If JSON parsing fails, return raw response
            return {
                'career': career,
                'explanation': response,
                'key_strengths': [],
                'roadmap': [],
                'considerations': '',
                'source': 'bedrock_raw'
            }
    
    def _fallback_explanation(self) -> str:
        """Fallback explanation if Bedrock fails"""
        return json.dumps({
            "explanation": "This career matches your profile based on our analysis of your skills, education, and interests.",
            "key_strengths": [
                "Strong alignment with your current skill set",
                "Compatible with your educational background",
                "Good opportunities in your region"
            ],
            "roadmap": [
                "Step 1: Complete relevant education/certification",
                "Step 2: Build foundational skills through projects",
                "Step 3: Gain practical experience through internships",
                "Step 4: Network with professionals in the field",
                "Step 5: Apply for entry-level positions"
            ],
            "considerations": "Consider exploring related fields and continuously updating your skills."
        })
