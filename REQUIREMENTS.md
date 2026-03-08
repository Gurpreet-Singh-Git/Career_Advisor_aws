# Requirements Document

## AI-Powered Career Guidance System for Indian Students

**Version:** 1.0  
**Date:** March 2026  
**Project:** AWS Hackathon - AI for Bharat

---

## 1. Project Overview

### 1.1 Purpose
Build a production-ready, AI-powered career guidance platform that provides personalized career recommendations to Indian students using AWS-native services, combining explainable Machine Learning with AWS Bedrock AI.

### 1.2 Target Users
- Indian students (10th, 12th, undergraduate, postgraduate)
- Age group: 15-25 years
- Potential reach: 50+ million students
- Geographic focus: India (all states and cities)

### 1.3 Core Problem
- Limited access to personalized career guidance
- Overwhelming number of career options (500+ careers)
- Lack of transparency in recommendation systems
- Need for context-aware advice (Indian education system, job market)
- Privacy concerns with personal data

---

## 2. Functional Requirements

### 2.1 User Interaction

#### FR-1: Natural Language Chat Interface
- **Priority:** High
- **Description:** Users can interact with the system using natural language
- **Acceptance Criteria:**
  - Support conversational queries (e.g., "Is BTech worth it in 2026?")
  - Provide contextual responses using AWS Bedrock
  - Handle exploration mode (general questions)
  - Detect intent for personalized recommendations
  - Response time < 3 seconds

#### FR-2: Intent Detection
- **Priority:** High
- **Description:** System detects user intent before collecting personal data
- **Acceptance Criteria:**
  - Distinguish between exploration and personalization requests
  - No data collection during exploration mode
  - Trigger consent flow only when personalization is requested
  - Accuracy > 90%

#### FR-3: Consent Management
- **Priority:** Critical
- **Description:** Explicit user consent before collecting personal information
- **Acceptance Criteria:**
  - Clear consent prompt explaining data usage
  - Option to decline and continue exploration
  - Session-only data storage
  - No permanent storage without explicit permission
  - Compliance with privacy regulations

### 2.2 Career Recommendation

#### FR-4: Career Ranking Engine
- **Priority:** High
- **Description:** ML-based ranking system for career recommendations
- **Acceptance Criteria:**
  - Input: education level, skills, interests, location
  - Output: Top 3 career recommendations with scores
  - Explainable scoring with breakdown
  - Weighted algorithm:
    - Skill match: 35%
    - Education fit: 25%
    - Interest alignment: 25%
    - Regional demand: 15%
  - Processing time < 2 seconds

#### FR-5: Personalized Explanations
- **Priority:** High
- **Description:** AI-generated explanations for each recommendation
- **Acceptance Criteria:**
  - Use AWS Bedrock (Claude) for generation
  - Include "why this career fits you"
  - Provide personalized roadmap
  - Context-aware (Indian education system)
  - Length: 150-300 words per career

#### FR-6: Score Transparency
- **Priority:** High
- **Description:** Display detailed score breakdown for each recommendation
- **Acceptance Criteria:**
  - Show individual component scores
  - Visual representation (progress bars/charts)
  - Explain scoring methodology
  - Allow users to understand decision-making

### 2.3 Data Management

#### FR-7: Career Database
- **Priority:** High
- **Description:** Comprehensive database of Indian career options
- **Acceptance Criteria:**
  - Minimum 10 careers (expandable to 100+)
  - Include: title, description, required education, skills, salary range
  - Indian context (INR salaries, Indian cities)
  - Regular updates capability

#### FR-8: User Profile Collection
- **Priority:** High
- **Description:** Structured form for collecting user information
- **Acceptance Criteria:**
  - Fields: education level, skills (multi-select), interests, location
  - Validation for all inputs
  - Optional fields clearly marked
  - Mobile-responsive design
  - Save/edit capability within session

#### FR-9: Session Management
- **Priority:** Medium
- **Description:** Temporary storage of user data during session
- **Acceptance Criteria:**
  - Session-based storage (no permanent DB)
  - Session ID generation
  - Data cleared after session ends
  - No cross-session data persistence

---

## 3. Non-Functional Requirements

### 3.1 Performance

#### NFR-1: Response Time
- Chat responses: < 3 seconds
- Career ranking: < 2 seconds
- Explanation generation: < 5 seconds
- Page load time: < 2 seconds

#### NFR-2: Scalability
- Support 1000+ concurrent users
- Auto-scaling with AWS Lambda
- Handle 10,000+ requests per day
- Cost per user: < $0.05

#### NFR-3: Availability
- Uptime: 99.9%
- Serverless architecture (no server maintenance)
- Multi-region deployment capability
- Automatic failover

### 3.2 Security

#### NFR-4: Data Privacy
- No permanent storage of personal data
- Session-only data retention
- HTTPS encryption for all communications
- No third-party data sharing
- Compliance with data protection regulations

#### NFR-5: Authentication
- No user authentication required (anonymous access)
- Session-based identification only
- No password storage
- No email collection

### 3.3 Usability

#### NFR-6: User Interface
- Clean, modern design
- Mobile-responsive (works on all devices)
- Accessibility compliant
- Intuitive navigation
- Clear call-to-action buttons

#### NFR-7: User Experience
- Minimal clicks to get recommendations (< 5 clicks)
- Clear progress indicators
- Error messages in plain language
- Option to restart/go back at any step

### 3.4 Maintainability

#### NFR-8: Code Quality
- Modular architecture
- Clear separation of concerns
- Comprehensive documentation
- Unit tests for critical functions
- Code comments for complex logic

#### NFR-9: Deployment
- Automated deployment pipeline
- Infrastructure as Code
- Easy rollback capability
- Environment-based configuration

---

## 4. Technical Requirements

### 4.1 AWS Services (Mandatory)

#### TR-1: AWS Bedrock
- **Purpose:** AI conversations and explanations
- **Model:** Claude 3 Sonnet
- **Usage:**
  - Natural language chat
  - Intent detection support
  - Personalized explanation generation
- **Requirement:** Must be PRIMARY AI service

#### TR-2: AWS Lambda
- **Purpose:** Serverless compute
- **Usage:**
  - API endpoints
  - Business logic execution
  - Integration layer
- **Configuration:**
  - Runtime: Python 3.11
  - Memory: 512MB - 1GB
  - Timeout: 30 seconds

#### TR-3: API Gateway
- **Purpose:** API management
- **Usage:**
  - REST API endpoints
  - Request routing
  - CORS configuration
- **Endpoints:**
  - POST /api/chat
  - POST /api/rank-careers
  - POST /api/explain-career
  - GET /api/health

#### TR-4: DynamoDB (Optional)
- **Purpose:** Session storage
- **Usage:**
  - Temporary user sessions
  - Career data cache
- **Configuration:**
  - On-demand pricing
  - TTL enabled (auto-delete after 24 hours)

#### TR-5: S3
- **Purpose:** Static hosting and data storage
- **Usage:**
  - Frontend hosting
  - Career database storage
  - Static assets
- **Configuration:**
  - Public read access for frontend
  - Versioning enabled

#### TR-6: CloudFront
- **Purpose:** CDN for frontend
- **Usage:**
  - Fast content delivery
  - HTTPS enforcement
  - Global distribution

### 4.2 Technology Stack

#### TR-7: Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI-style (Lambda compatible)
- **Libraries:**
  - boto3 (AWS SDK)
  - scikit-learn (ML ranking)
  - pandas (data processing)

#### TR-8: Frontend
- **Framework:** React 18.2+
- **Language:** JavaScript (ES6+)
- **Libraries:**
  - react-dom
  - react-scripts
- **Styling:** CSS3

#### TR-9: Deployment
- **Platform:** Vercel (frontend) + AWS (backend)
- **CI/CD:** GitHub integration
- **Configuration:** vercel.json, AWS SAM/CloudFormation

### 4.3 Machine Learning

#### TR-10: Ranking Algorithm
- **Type:** Weighted scoring model
- **Features:**
  - Skill matching (TF-IDF or keyword matching)
  - Education level compatibility
  - Interest alignment
  - Regional demand factors
- **Output:** Normalized scores (0-100)

#### TR-11: Explainability
- **Method:** Score breakdown display
- **Components:**
  - Individual feature scores
  - Weight explanation
  - Visual representation
- **Transparency:** Full algorithm disclosure

---

## 5. Integration Requirements

### 5.1 AWS Bedrock Integration

#### IR-1: Chat Integration
- Use Claude 3 Sonnet model
- Implement prompt templates
- Handle streaming responses (optional)
- Error handling and fallback

#### IR-2: Explanation Generation
- Context-aware prompts
- Include user profile in context
- Include score breakdown in prompt
- Generate structured output

### 5.2 Frontend-Backend Integration

#### IR-3: API Communication
- RESTful API design
- JSON request/response format
- Error handling with status codes
- CORS configuration

#### IR-4: State Management
- React state for UI
- Session storage for temporary data
- No persistent local storage

---

## 6. Data Requirements

### 6.1 Career Data Schema

```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "required_education": ["array of strings"],
  "required_skills": ["array of strings"],
  "interests": ["array of strings"],
  "salary_range": {
    "min": "number (INR)",
    "max": "number (INR)"
  },
  "growth_rate": "string",
  "demand_cities": ["array of strings"]
}
```

### 6.2 User Profile Schema

```json
{
  "education_level": "string",
  "skills": ["array of strings"],
  "interests": ["array of strings"],
  "location": "string",
  "session_id": "string"
}
```

### 6.3 Recommendation Output Schema

```json
{
  "careers": [
    {
      "title": "string",
      "score": "number (0-100)",
      "breakdown": {
        "skill_match": "number",
        "education_fit": "number",
        "interest_alignment": "number",
        "regional_demand": "number"
      },
      "explanation": "string"
    }
  ]
}
```

---

## 7. Compliance Requirements

### 7.1 Privacy

#### CR-1: Data Protection
- No permanent storage of personal data
- Session-only retention
- Clear privacy policy
- User consent before data collection

#### CR-2: Transparency
- Explain how recommendations are made
- Show scoring methodology
- Disclose AI usage
- Provide disclaimer (recommendations, not guarantees)

### 7.2 Ethical AI

#### CR-3: Fairness
- No bias based on gender, caste, religion
- Equal recommendations for all users
- Transparent scoring (no black-box)

#### CR-4: Responsibility
- Clear disclaimers
- No guarantees of career success
- Encourage informed decision-making
- Provide multiple options (not single recommendation)

---

## 8. Testing Requirements

### 8.1 Unit Testing

#### TR-12: Backend Tests
- Test career ranking algorithm
- Test intent detection
- Test API endpoints
- Test AWS Bedrock integration

#### TR-13: Frontend Tests
- Test component rendering
- Test form validation
- Test API calls
- Test error handling

### 8.2 Integration Testing

#### TR-14: End-to-End Tests
- Test complete user flow
- Test chat → form → results
- Test error scenarios
- Test edge cases

### 8.3 Performance Testing

#### TR-15: Load Testing
- Test with 100+ concurrent users
- Measure response times
- Test AWS Lambda scaling
- Monitor costs

---

## 9. Documentation Requirements

### 9.1 Technical Documentation

#### DR-1: Architecture Documentation
- System architecture diagram
- AWS service integration
- Data flow diagrams
- API documentation

#### DR-2: Code Documentation
- Inline code comments
- Function/class documentation
- README files
- Setup instructions

### 9.2 User Documentation

#### DR-3: User Guide
- How to use the system
- FAQ section
- Privacy policy
- Disclaimer

---

## 10. Success Criteria

### 10.1 Functional Success
- ✅ Users can chat with AI
- ✅ Users can get personalized recommendations
- ✅ Recommendations are explainable
- ✅ System respects privacy
- ✅ All AWS services integrated

### 10.2 Technical Success
- ✅ Response time < 3 seconds
- ✅ 99.9% uptime
- ✅ Cost < $0.05 per user
- ✅ Scalable to 1000+ concurrent users
- ✅ Production-ready deployment

### 10.3 Business Success
- ✅ Solves real problem for Indian students
- ✅ Demonstrates AWS Bedrock capabilities
- ✅ Showcases serverless architecture
- ✅ Production-ready for 50M+ users
- ✅ Cost-effective solution

---

## 11. Out of Scope

### 11.1 Not Included in V1.0
- User authentication/login
- Permanent user profiles
- Payment integration
- Course recommendations
- College recommendations
- Job search integration
- Mobile app (native)
- Multi-language support
- Advanced analytics dashboard

### 11.2 Future Enhancements
- RAG (Retrieval Augmented Generation) for career info
- Real-time job market data integration
- Skill gap analysis
- Learning path recommendations
- Career counselor chat
- Video content integration

---

## 12. Constraints

### 12.1 Technical Constraints
- Must use AWS Bedrock as primary AI service
- Serverless architecture (no EC2 instances)
- Budget: < $100/month for 10,000 users
- Development time: 2-3 weeks

### 12.2 Business Constraints
- Target: AWS Hackathon submission
- Focus: Indian student market
- Privacy-first approach (no data collection without consent)
- Free for end users

---

## 13. Assumptions

1. Users have internet access
2. Users can read English
3. AWS Bedrock is available in deployment region
4. Career data is manually curated (not real-time)
5. Users provide accurate information in forms
6. Session duration < 1 hour
7. Users access via web browser (not mobile app)

---

## 14. Dependencies

### 14.1 External Dependencies
- AWS account with Bedrock access
- GitHub account for code hosting
- Vercel account for frontend deployment
- Domain name (optional)

### 14.2 Internal Dependencies
- Career database must be created before ranking
- Frontend depends on backend API
- Explanations depend on ranking results
- All features depend on AWS Bedrock availability

---

## 15. Risks and Mitigations

### 15.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| AWS Bedrock unavailable | High | Low | Implement fallback responses |
| High AWS costs | Medium | Medium | Set billing alerts, optimize prompts |
| Slow response times | Medium | Low | Optimize Lambda, use caching |
| Scaling issues | High | Low | Use AWS auto-scaling, load testing |

### 15.2 Business Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Low user adoption | Medium | Medium | Focus on UX, clear value proposition |
| Privacy concerns | High | Low | Clear privacy policy, consent flow |
| Inaccurate recommendations | High | Medium | Test with real users, iterate |
| Competition | Low | High | Focus on explainability, AWS integration |

---

## 16. Approval

**Prepared by:** Development Team  
**Date:** March 2026  
**Status:** Approved  
**Version:** 1.0

---

**Document Control:**
- Last Updated: March 2026
- Next Review: After hackathon submission
- Owner: Project Team
