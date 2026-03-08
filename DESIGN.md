# Design Document

## AI-Powered Career Guidance System for Indian Students

**Version:** 1.0  
**Date:** March 2026  
**Project:** AWS Hackathon - AI for Bharat

---

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER LAYER                          │
│  (Web Browser - Desktop/Mobile)                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  React Frontend (Vercel/CloudFront + S3)             │  │
│  │  - Chat Interface                                     │  │
│  │  - Career Form                                        │  │
│  │  - Results Display                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                       │
│  AWS API Gateway (REST API)                                 │
│  - /api/chat                                                │
│  - /api/rank-careers                                        │
│  - /api/explain-career                                      │
│  - /api/health                                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  AWS Lambda Functions (Python 3.11)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Intent     │  │   Career     │  │     LLM      │     │
│  │  Detection   │  │   Ranking    │  │ Explanation  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      AI/DATA LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ AWS Bedrock  │  │  DynamoDB    │  │      S3      │     │
│  │   (Claude)   │  │  (Sessions)  │  │  (Careers)   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Component Interaction Flow


```
User → Frontend → API Gateway → Lambda → Bedrock/ML → Response
  ↓                                  ↓
Chat                            DynamoDB (session)
  ↓                                  ↓
Form                            S3 (career data)
  ↓
Results
```

---

## 2. Detailed Component Design

### 2.1 Frontend Architecture (React)

#### 2.1.1 Component Structure

```
src/
├── App.js                    # Main application component
├── components/
│   ├── ChatInterface.js      # Chat UI component
│   ├── CareerForm.js         # User profile form
│   └── ResultsDisplay.js     # Recommendations display
├── services/
│   └── api.js                # API client (future)
└── App.css                   # Styling
```

#### 2.1.2 State Management

**App.js State:**
```javascript
{
  mode: 'chat' | 'form' | 'results',
  careerResults: {
    rankings: [...],
    explanations: [...]
  },
  loading: boolean
}
```

#### 2.1.3 User Flow

```
1. Landing (Chat Mode)
   ↓
2. User types question
   ↓
3. AI responds (AWS Bedrock)
   ↓
4. If personalization requested → Show consent
   ↓
5. If consent given → Show form (Form Mode)
   ↓
6. User fills form
   ↓
7. Submit → Get rankings + explanations
   ↓
8. Display results (Results Mode)
   ↓
9. Option to start over
```

### 2.2 Backend Architecture (Python Lambda)

#### 2.2.1 Module Structure

```
backend/
├── main.py                          # Lambda entry point
├── ai_chat/
│   └── bedrock_chat.py             # AWS Bedrock integration
├── intent_detection/
│   └── detector.py                 # Intent detection logic
├── career_ranking/
│   └── ranker.py                   # ML ranking engine
└── llm_explanation/
    └── explainer.py                # Explanation generation
```

#### 2.2.2 API Endpoints Design

**Endpoint 1: Chat**
```
POST /api/chat
Request:
{
  "message": "string",
  "session_id": "string"
}

Response:
{
  "response": "string",
  "requires_form": boolean,
  "source": "bedrock" | "fallback"
}
```

**Endpoint 2: Rank Careers**
```
POST /api/rank-careers
Request:
{
  "education_level": "string",
  "skills": ["array"],
  "interests": ["array"],
  "location": "string"
}

Response:
{
  "careers": [
    {
      "title": "string",
      "score": number,
      "breakdown": {
        "skill_match": number,
        "education_fit": number,
        "interest_alignment": number,
        "regional_demand": number
      }
    }
  ]
}
```

**Endpoint 3: Explain Career**
```
POST /api/explain-career
Request:
{
  "career": "string",
  "user_profile": {...},
  "score_breakdown": {...}
}

Response:
{
  "explanation": "string",
  "source": "bedrock" | "fallback"
}
```

### 2.3 AI Integration Design

#### 2.3.1 AWS Bedrock Integration

**Model:** Claude 3 Sonnet

**Use Cases:**
1. Natural language chat
2. Intent understanding
3. Personalized explanations

**Prompt Template for Chat:**
```python
prompt = f"""You are a career guidance counselor for Indian students.

User question: {user_message}

Provide a helpful, concise response. If the user wants personalized 
recommendations, suggest they fill out a profile form.

Keep responses under 100 words. Be encouraging and supportive.
"""
```

**Prompt Template for Explanations:**
```python
prompt = f"""Generate a personalized career explanation for an Indian student.

Career: {career_title}
Student Profile:
- Education: {education}
- Skills: {skills}
- Interests: {interests}
- Location: {location}

Score Breakdown:
- Skill Match: {skill_score}/100
- Education Fit: {edu_score}/100
- Interest Alignment: {interest_score}/100
- Regional Demand: {regional_score}/100

Provide:
1. Why this career fits them (2-3 sentences)
2. Personalized roadmap (3-4 steps)
3. Encouragement (1 sentence)

Keep it under 250 words. Use Indian context (INR, Indian cities, education system).
"""
```

#### 2.3.2 Fallback Mechanism

```python
def get_ai_response(prompt):
    try:
        # Try AWS Bedrock
        response = bedrock_client.invoke_model(...)
        return response, "bedrock"
    except Exception as e:
        # Fallback to template-based response
        response = generate_fallback_response(prompt)
        return response, "fallback"
```

### 2.4 Machine Learning Design

#### 2.4.1 Career Ranking Algorithm

**Algorithm Type:** Weighted Scoring Model

**Formula:**
```
Total_Score = (0.35 × Skill_Match) + 
              (0.25 × Education_Fit) + 
              (0.25 × Interest_Alignment) + 
              (0.15 × Regional_Demand)
```

**Component Calculations:**

**1. Skill Match (0-100):**
```python
def calculate_skill_match(user_skills, career_required_skills):
    matching_skills = set(user_skills) & set(career_required_skills)
    if len(career_required_skills) == 0:
        return 50  # neutral score
    match_ratio = len(matching_skills) / len(career_required_skills)
    return match_ratio * 100
```

**2. Education Fit (0-100):**
```python
education_hierarchy = {
    "10th": 1,
    "12th": 2,
    "Diploma": 3,
    "BTech": 4,
    "MTech": 5,
    "MBA": 5,
    "PhD": 6
}

def calculate_education_fit(user_education, career_required_education):
    user_level = education_hierarchy.get(user_education, 0)
    required_levels = [education_hierarchy.get(e, 0) 
                      for e in career_required_education]
    
    if user_level >= max(required_levels):
        return 100  # fully qualified
    elif user_level >= min(required_levels):
        return 70   # partially qualified
    else:
        return 30   # under-qualified
```

**3. Interest Alignment (0-100):**
```python
def calculate_interest_alignment(user_interests, career_interests):
    matching_interests = set(user_interests) & set(career_interests)
    if len(career_interests) == 0:
        return 50  # neutral
    match_ratio = len(matching_interests) / len(career_interests)
    return match_ratio * 100
```

**4. Regional Demand (0-100):**
```python
def calculate_regional_demand(user_location, career_demand_cities):
    if user_location in career_demand_cities:
        return 100  # high demand in user's city
    
    # Check if nearby cities have demand
    nearby_cities = get_nearby_cities(user_location)
    if any(city in career_demand_cities for city in nearby_cities):
        return 70   # demand in nearby cities
    
    return 40  # general demand
```

#### 2.4.2 Ranking Process

```python
def rank_careers(user_profile, careers_db):
    scored_careers = []
    
    for career in careers_db:
        # Calculate component scores
        skill_score = calculate_skill_match(
            user_profile['skills'], 
            career['required_skills']
        )
        education_score = calculate_education_fit(
            user_profile['education_level'],
            career['required_education']
        )
        interest_score = calculate_interest_alignment(
            user_profile['interests'],
            career['interests']
        )
        regional_score = calculate_regional_demand(
            user_profile['location'],
            career['demand_cities']
        )
        
        # Calculate total score
        total_score = (
            0.35 * skill_score +
            0.25 * education_score +
            0.25 * interest_score +
            0.15 * regional_score
        )
        
        scored_careers.append({
            'career': career,
            'total_score': total_score,
            'breakdown': {
                'skill_match': skill_score,
                'education_fit': education_score,
                'interest_alignment': interest_score,
                'regional_demand': regional_score
            }
        })
    
    # Sort by score and return top 3
    scored_careers.sort(key=lambda x: x['total_score'], reverse=True)
    return scored_careers[:3]
```

---

## 3. Data Design

### 3.1 Career Data Schema

**Storage:** S3 (JSON file)

**Schema:**
```json
{
  "careers": [
    {
      "id": "career_001",
      "title": "Software Engineer",
      "description": "Develop and maintain software applications",
      "required_education": ["BTech", "MTech", "Diploma"],
      "required_skills": [
        "Python",
        "JavaScript",
        "Problem Solving",
        "Data Structures"
      ],
      "interests": [
        "Technology",
        "Problem Solving",
        "Innovation"
      ],
      "salary_range": {
        "min": 400000,
        "max": 2000000,
        "currency": "INR"
      },
      "growth_rate": "High",
      "demand_cities": [
        "Bangalore",
        "Hyderabad",
        "Pune",
        "Mumbai",
        "Delhi"
      ],
      "industry": "Technology"
    }
  ]
}
```

### 3.2 Session Data Schema

**Storage:** DynamoDB (optional) or in-memory

**Schema:**
```json
{
  "session_id": "session_12345",
  "created_at": "2026-03-07T18:00:00Z",
  "ttl": 1709838000,
  "user_profile": {
    "education_level": "BTech",
    "skills": ["Python", "JavaScript"],
    "interests": ["Technology", "Innovation"],
    "location": "Bangalore"
  },
  "conversation_history": [
    {
      "role": "user",
      "message": "What are good tech careers?"
    },
    {
      "role": "assistant",
      "message": "There are many exciting tech careers..."
    }
  ]
}
```

### 3.3 Database Design (DynamoDB)

**Table: user_sessions**

| Attribute | Type | Description |
|-----------|------|-------------|
| session_id (PK) | String | Unique session identifier |
| created_at | Number | Unix timestamp |
| ttl | Number | Time to live (24 hours) |
| user_profile | Map | User information |
| conversation_history | List | Chat messages |

**Indexes:** None (simple key-value lookup)

**TTL:** 24 hours (auto-delete old sessions)

---

## 4. Security Design

### 4.1 Authentication & Authorization

**Approach:** No authentication required
- Anonymous access
- Session-based identification
- No user accounts

### 4.2 Data Protection

**In Transit:**
- HTTPS/TLS 1.3 for all communications
- API Gateway enforces HTTPS
- CloudFront SSL certificates

**At Rest:**
- S3 server-side encryption
- DynamoDB encryption at rest
- No sensitive data stored permanently

### 4.3 Privacy Design

**Principles:**
1. **Consent First:** No data collection without explicit consent
2. **Session Only:** Data deleted after session ends
3. **Transparency:** Clear explanation of data usage
4. **Minimal Collection:** Only collect necessary information

**Implementation:**
```javascript
// Frontend consent flow
const handleConsent = () => {
  const consent = window.confirm(
    "To provide personalized recommendations, we need to collect " +
    "your education, skills, interests, and location. " +
    "This data will only be used for this session and not stored permanently. " +
    "Do you consent?"
  );
  
  if (consent) {
    setMode('form');
  }
};
```

### 4.4 API Security

**Rate Limiting:**
- API Gateway throttling: 1000 requests/second
- Per-user limit: 10 requests/minute

**CORS Configuration:**
```json
{
  "allowOrigins": ["*"],
  "allowMethods": ["GET", "POST", "OPTIONS"],
  "allowHeaders": ["Content-Type", "Authorization"],
  "maxAge": 3600
}
```

**Input Validation:**
- Validate all user inputs
- Sanitize strings
- Limit input lengths
- Reject malformed requests

---

## 5. Performance Design

### 5.1 Response Time Optimization

**Target Response Times:**
- Chat: < 3 seconds
- Ranking: < 2 seconds
- Explanation: < 5 seconds

**Optimization Strategies:**

**1. Lambda Optimization:**
```python
# Keep Lambda warm
def lambda_handler(event, context):
    # Reuse connections
    global bedrock_client
    if bedrock_client is None:
        bedrock_client = boto3.client('bedrock-runtime')
    
    # Process request
    return process_request(event)
```

**2. Caching:**
- Cache career data in Lambda memory
- Cache common AI responses
- Use CloudFront for static assets

**3. Parallel Processing:**
```python
# Get explanations in parallel
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(get_explanation, career)
        for career in top_careers
    ]
    explanations = [f.result() for f in futures]
```

### 5.2 Scalability Design

**Auto-Scaling:**
- Lambda: Automatic (up to 1000 concurrent executions)
- API Gateway: Automatic
- DynamoDB: On-demand capacity

**Load Distribution:**
- CloudFront: Global CDN
- Multi-region deployment (future)

**Cost Optimization:**
- Lambda: Pay per request
- DynamoDB: On-demand pricing
- S3: Lifecycle policies

---

## 6. Error Handling Design

### 6.1 Error Categories

**1. User Errors (4xx):**
- Invalid input
- Missing required fields
- Malformed requests

**2. System Errors (5xx):**
- AWS service unavailable
- Lambda timeout
- Database errors

**3. AI Errors:**
- Bedrock unavailable
- Model errors
- Prompt failures

### 6.2 Error Handling Strategy

**Frontend:**
```javascript
try {
  const response = await fetch('/api/chat', {...});
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  const data = await response.json();
} catch (error) {
  // User-friendly error message
  alert('Failed to process request. Please try again.');
  console.error('Error:', error);
}
```

**Backend:**
```python
def lambda_handler(event, context):
    try:
        # Process request
        result = process_request(event)
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except ValidationError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
```

### 6.3 Fallback Mechanisms

**AI Fallback:**
```python
def get_ai_response(prompt):
    try:
        return bedrock_response(prompt), "bedrock"
    except:
        return template_response(prompt), "fallback"
```

**Data Fallback:**
- If DynamoDB unavailable → Use in-memory storage
- If S3 unavailable → Use embedded career data

---

## 7. Deployment Design

### 7.1 Deployment Architecture

**Frontend:**
- Platform: Vercel
- Build: React production build
- CDN: Vercel Edge Network
- Domain: Auto-generated or custom

**Backend:**
- Platform: AWS Lambda
- Deployment: AWS SAM / CloudFormation
- API: API Gateway
- Region: us-east-1 (or closest to India)

### 7.2 CI/CD Pipeline

```
GitHub Push
    ↓
Vercel Auto-Deploy (Frontend)
    ↓
Build React App
    ↓
Deploy to Vercel CDN
    ↓
Update DNS
    ↓
Live!
```

### 7.3 Environment Configuration

**Development:**
- Local React dev server
- Mock API responses
- No AWS services

**Production:**
- Vercel frontend
- AWS Lambda backend
- Real AWS Bedrock
- DynamoDB sessions

---

## 8. Monitoring & Logging Design

### 8.1 Logging Strategy

**Frontend:**
- Console logs for debugging
- Error tracking (optional: Sentry)

**Backend:**
- CloudWatch Logs for Lambda
- Structured logging (JSON format)
- Log levels: INFO, WARN, ERROR

**Log Format:**
```json
{
  "timestamp": "2026-03-07T18:00:00Z",
  "level": "INFO",
  "service": "career-ranking",
  "message": "Ranked careers for user",
  "session_id": "session_12345",
  "duration_ms": 150
}
```

### 8.2 Metrics

**Key Metrics:**
- Request count
- Response time (p50, p95, p99)
- Error rate
- AWS Bedrock usage
- Lambda invocations
- Cost per request

**Monitoring Tools:**
- CloudWatch Metrics
- CloudWatch Dashboards
- Billing alerts

---

## 9. Testing Design

### 9.1 Unit Testing

**Backend Tests:**
```python
def test_skill_match():
    user_skills = ["Python", "JavaScript"]
    career_skills = ["Python", "Java", "JavaScript"]
    score = calculate_skill_match(user_skills, career_skills)
    assert score == 66.67  # 2/3 match
```

**Frontend Tests:**
```javascript
test('renders chat interface', () => {
  render(<ChatInterface />);
  expect(screen.getByText(/Ask me anything/i)).toBeInTheDocument();
});
```

### 9.2 Integration Testing

**End-to-End Flow:**
1. User sends chat message
2. System responds with AI
3. User requests personalization
4. System shows consent
5. User fills form
6. System returns recommendations
7. User views results

### 9.3 Performance Testing

**Load Test Scenarios:**
- 100 concurrent users
- 1000 requests/minute
- Sustained load for 10 minutes

**Tools:**
- Apache JMeter
- AWS Load Testing
- Locust

---

## 10. Future Enhancements

### 10.1 Phase 2 Features

**RAG Integration:**
- Store career documents in vector DB
- Use embeddings for semantic search
- Provide more detailed career information

**Real-time Data:**
- Integrate job market APIs
- Live salary data
- Current demand trends

**Advanced ML:**
- Collaborative filtering
- Deep learning models
- Personalized learning paths

### 10.2 Scalability Improvements

**Multi-Region:**
- Deploy in multiple AWS regions
- Route53 for geo-routing
- Reduce latency for global users

**Caching Layer:**
- ElastiCache for Redis
- Cache common queries
- Reduce Bedrock costs

---

## 11. Design Decisions & Rationale

### 11.1 Why Serverless?

**Decision:** Use AWS Lambda instead of EC2

**Rationale:**
- Auto-scaling (handle traffic spikes)
- Pay per request (cost-effective)
- No server management
- High availability built-in

### 11.2 Why React?

**Decision:** Use React for frontend

**Rationale:**
- Component-based architecture
- Large ecosystem
- Easy to deploy on Vercel
- Good performance

### 11.3 Why Weighted Scoring?

**Decision:** Use weighted scoring instead of deep learning

**Rationale:**
- Explainable (transparent to users)
- Fast (< 2 seconds)
- No training data required
- Easy to adjust weights

### 11.4 Why Session-Only Storage?

**Decision:** Don't store user data permanently

**Rationale:**
- Privacy-first approach
- No GDPR compliance needed
- Simpler architecture
- Lower costs

---

## 12. Design Constraints

### 12.1 Technical Constraints

- Must use AWS Bedrock (hackathon requirement)
- Serverless only (no EC2)
- Budget: < $100/month
- Response time: < 5 seconds

### 12.2 Business Constraints

- Free for users
- Indian market focus
- Privacy-first
- Production-ready

---

## 13. Design Validation

### 13.1 Architecture Review Checklist

- ✅ Scalable to 1000+ concurrent users
- ✅ Response time < 5 seconds
- ✅ Cost < $0.05 per user
- ✅ Privacy-compliant
- ✅ AWS Bedrock integrated
- ✅ Explainable recommendations
- ✅ Production-ready

### 13.2 Security Review Checklist

- ✅ HTTPS enforced
- ✅ Input validation
- ✅ No sensitive data stored
- ✅ Rate limiting enabled
- ✅ CORS configured
- ✅ Error handling implemented

---

## 14. Appendix

### 14.1 Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 18.2 | UI components |
| Hosting | Vercel | Frontend deployment |
| API | AWS API Gateway | REST endpoints |
| Compute | AWS Lambda | Serverless functions |
| AI | AWS Bedrock (Claude) | Chat & explanations |
| Database | DynamoDB | Session storage |
| Storage | S3 | Career data |
| CDN | CloudFront | Content delivery |

### 14.2 AWS Services Usage

| Service | Usage | Cost Estimate |
|---------|-------|---------------|
| Bedrock | 10K requests/month | $30 |
| Lambda | 100K invocations | $2 |
| API Gateway | 100K requests | $3.50 |
| DynamoDB | 10K reads/writes | $2.50 |
| S3 | 1GB storage | $0.02 |
| CloudFront | 10GB transfer | $0.85 |
| **Total** | | **~$39/month** |

---

**Document Control:**
- Version: 1.0
- Last Updated: March 2026
- Status: Approved
- Owner: Development Team
