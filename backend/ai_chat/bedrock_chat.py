"""
AWS Bedrock Chat Integration
Dynamic AI-powered conversations using Claude
"""
import json

try:
    import boto3
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

class BedrockChat:
    """AI-powered chat using AWS Bedrock"""
    
    def __init__(self):
        if HAS_BOTO3:
            self.bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
            self.model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
        else:
            self.bedrock_client = None
        
        # System prompt for career guidance context
        self.system_prompt = """You are an AI career guidance assistant for Indian students. Your role is to:

1. Answer career-related questions naturally and conversationally
2. Provide information about careers, education paths, skills, and job markets in India
3. When users ask about specific careers, provide detailed information about:
   - Required education and skills
   - Career prospects in India
   - Salary ranges in INR
   - Growth opportunities
   - Challenges and considerations

4. When users want personalized recommendations, guide them to fill the form by saying:
   "I'd be happy to provide personalized career recommendations! To give you the best suggestions, I'll need to know about your education, skills, interests, and location. Would you like to fill out a quick form?"

5. Be encouraging, supportive, and realistic
6. Always consider the Indian education system and job market context
7. Use INR for salaries, mention Indian cities, and reference Indian institutions

Keep responses concise (2-3 paragraphs) and conversational."""
    
    def chat(self, message, conversation_history=None):
        """
        Send message to AI and get response
        
        Args:
            message: User's message
            conversation_history: List of previous messages (optional)
            
        Returns:
            dict with response and metadata
        """
        if HAS_BOTO3 and self.bedrock_client:
            return self._chat_with_bedrock(message, conversation_history)
        else:
            return self._chat_fallback(message)
    
    def _chat_with_bedrock(self, message, conversation_history):
        """Use AWS Bedrock for AI chat"""
        try:
            # Build conversation messages
            messages = []
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-5:]:  # Keep last 5 messages for context
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Prepare request
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "temperature": 0.7,
                "system": self.system_prompt,
                "messages": messages
            }
            
            # Call Bedrock
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            ai_response = response_body['content'][0]['text']
            
            # Detect if user wants personalized recommendations
            wants_personalized = self._detect_personalized_intent(message, ai_response)
            
            return {
                'response': ai_response,
                'source': 'bedrock',
                'requires_form': wants_personalized,
                'model': self.model_id
            }
            
        except Exception as e:
            print(f"Bedrock error: {str(e)}")
            return self._chat_fallback(message)
    
    def _chat_fallback(self, message):
        """Fallback response when Bedrock is not available"""
        message_lower = message.lower()
        
        # Check for personalized recommendation request
        if any(word in message_lower for word in ['recommend', 'personalized', 'for me', 'my profile', 'help me choose']):
            return {
                'response': "I'd be happy to provide personalized career recommendations! To give you the best suggestions based on your unique profile, I'll need to know about your education, skills, interests, and location. Would you like to fill out a quick form to get your top 3 career matches?",
                'source': 'fallback',
                'requires_form': True
            }
        
        # Check for specific career questions
        elif any(word in message_lower for word in ['btech', 'engineering', 'software', 'data scientist', 'career']):
            if 'worth' in message_lower or 'should i' in message_lower:
                return {
                    'response': "That's a great question! The value of pursuing B.Tech in 2026 depends on several factors:\n\n1. **Strong Demand**: Technology careers remain in high demand in India, especially in cities like Bangalore, Hyderabad, and Pune. Software engineers and data scientists continue to have excellent job prospects.\n\n2. **Evolving Skills**: While a B.Tech degree provides a strong foundation, the tech industry values practical skills and continuous learning. Focus on building projects, learning in-demand technologies, and gaining internship experience.\n\n3. **Consider Your Interests**: B.Tech is worth it if you're genuinely interested in technology and problem-solving. If you'd like personalized career recommendations based on your specific interests and skills, I can help with that!",
                    'source': 'fallback',
                    'requires_form': False
                }
            else:
                return {
                    'response': "I can help you explore various career options in technology and engineering! India has a thriving tech industry with opportunities in software development, data science, AI/ML, cloud computing, and more.\n\nWould you like to:\n1. Learn about specific careers in detail\n2. Get personalized recommendations based on your profile\n3. Understand education paths and requirements\n\nJust let me know what interests you!",
                    'source': 'fallback',
                    'requires_form': False
                }
        
        # General career exploration
        else:
            return {
                'response': "I'm here to help you with career guidance! I can:\n\n• Answer questions about specific careers\n• Explain education paths and requirements\n• Discuss job market trends in India\n• Provide personalized career recommendations\n\nWhat would you like to know about careers?",
                'source': 'fallback',
                'requires_form': False
            }
    
    def _detect_personalized_intent(self, user_message, ai_response):
        """Detect if user wants personalized recommendations"""
        message_lower = user_message.lower()
        response_lower = ai_response.lower()
        
        # Check user message
        personalized_keywords = ['recommend', 'personalized', 'for me', 'my profile', 
                                'help me choose', 'what career should i', 'best career for me']
        
        # Check if AI suggested filling form
        form_keywords = ['fill out', 'form', 'questionnaire', 'tell me about your']
        
        user_wants = any(keyword in message_lower for keyword in personalized_keywords)
        ai_suggests = any(keyword in response_lower for keyword in form_keywords)
        
        return user_wants or ai_suggests
