"""
Intent Detection Module
Rule-based classifier to detect user intent before collecting personal data
"""
import re

class IntentDetector:
    """Detects user intent from natural language input"""
    
    def __init__(self):
        # Define intent patterns (rule-based)
        # Order matters: check personalized_guidance first!
        self.patterns = {
            'personalized_guidance': [
                r'\bpersonalized\b',
                r'\brecommend(ation)?s?\b',
                r'\bsuggest(ion)?s?\b',
                r'\bhelp me (choose|find|select)',
                r'\bguide me\b',
                r'\bwhat\s+career\s+(should|can)\s+i',
                r'\bbest\s+career\s+for\s+me',
                r'\bmy\s+(skills|interests|background|profile)',
                r'\bfor me\b',
            ],
            'exploration': [
                r'\b(explore|discover|learn about|what are|tell me about)\b.*\bcareer',
                r'\bcareer\s+(options|paths|choices)',
                r'\bjust\s+(looking|browsing)',
            ],
            'information_query': [
                r'\bhow\s+to\s+become',
                r'\bwhat\s+does\s+a\s+\w+\s+do',
                r'\bsalary|education|requirements',
            ]
        }
    
    def detect(self, message):
        """
        Detect intent from user message
        
        Args:
            message (str): User input message
            
        Returns:
            dict: Intent classification result
        """
        message_lower = message.lower()
        
        # Check personalized_guidance first (highest priority)
        for pattern in self.patterns['personalized_guidance']:
            if re.search(pattern, message_lower):
                return self._format_response('personalized_guidance', message)
        
        # Then check other intents
        for intent in ['information_query', 'exploration']:
            for pattern in self.patterns[intent]:
                if re.search(pattern, message_lower):
                    return self._format_response(intent, message)
        
        # Default to exploration if unclear
        return self._format_response('exploration', message)
    
    def _format_response(self, intent, message):
        """Format detection response with consent requirements"""
        
        # Determine if consent is needed
        requires_consent = intent == 'personalized_guidance'
        
        response = {
            'intent': intent,
            'requires_consent': requires_consent,
            'message': self._get_intent_message(intent),
            'original_query': message
        }
        
        if requires_consent:
            response['consent_prompt'] = (
                "To provide personalized career recommendations, I'll need to ask "
                "about your education, skills, interests, and location. "
                "This information will only be used for this session and won't be "
                "permanently stored. Do you consent to proceed?"
            )
        
        return response
    
    def _get_intent_message(self, intent):
        """Get appropriate message for detected intent"""
        messages = {
            'exploration': (
                "I can help you explore various career options available in India. "
                "Would you like to see popular career paths, or get personalized recommendations?"
            ),
            'personalized_guidance': (
                "I can provide personalized career recommendations based on your profile. "
                "I'll need some information about you to give the best suggestions."
            ),
            'information_query': (
                "I can provide detailed information about specific careers. "
                "What would you like to know?"
            )
        }
        return messages.get(intent, messages['exploration'])
