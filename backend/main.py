"""
Main Lambda handler for Career Guidance API
Routes requests to appropriate modules
"""
import json
import os
from intent_detection.detector import IntentDetector
from career_ranking.ranker import CareerRanker
from llm_explanation.explainer import CareerExplainer

# Initialize modules
intent_detector = IntentDetector()
career_ranker = CareerRanker()
career_explainer = CareerExplainer()

def lambda_handler(event, context):
    """Main Lambda handler"""
    try:
        # Parse request
        path = event.get('path', '')
        method = event.get('httpMethod', 'GET')
        body = json.loads(event.get('body', '{}'))
        
        # Route to appropriate handler
        if path == '/api/detect-intent' and method == 'POST':
            return handle_intent_detection(body)
        elif path == '/api/rank-careers' and method == 'POST':
            return handle_career_ranking(body)
        elif path == '/api/explain-career' and method == 'POST':
            return handle_career_explanation(body)
        elif path == '/api/health' and method == 'GET':
            return success_response({'status': 'healthy'})
        else:
            return error_response('Route not found', 404)
            
    except Exception as e:
        return error_response(str(e), 500)

def handle_intent_detection(body):
    """Detect user intent from message"""
    message = body.get('message', '')
    if not message:
        return error_response('Message is required', 400)
    
    result = intent_detector.detect(message)
    return success_response(result)

def handle_career_ranking(body):
    """Rank careers based on user profile"""
    # Validate required fields
    required = ['education', 'skills', 'interests', 'location']
    if not all(field in body for field in required):
        return error_response(f'Missing required fields: {required}', 400)
    
    # Rank careers
    rankings = career_ranker.rank(
        education=body['education'],
        skills=body['skills'],
        interests=body['interests'],
        location=body['location']
    )
    
    return success_response({'careers': rankings})

def handle_career_explanation(body):
    """Generate LLM explanation for career recommendation"""
    required = ['career', 'user_profile', 'score_breakdown']
    if not all(field in body for field in required):
        return error_response(f'Missing required fields: {required}', 400)
    
    explanation = career_explainer.explain(
        career=body['career'],
        user_profile=body['user_profile'],
        score_breakdown=body['score_breakdown']
    )
    
    return success_response(explanation)

def success_response(data):
    """Format success response"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(data)
    }

def error_response(message, status_code=400):
    """Format error response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'error': message})
    }
