# 🎓 AI-Powered Career Guidance System for Indian Students

## AWS Hackathon Submission - AI for Bharat

### Project Overview

An intelligent, serverless career guidance platform that combines explainable Machine Learning with AWS Bedrock AI to provide personalized career recommendations for Indian students. The system uses transparent ML scoring for decision-making and AWS Bedrock (Claude) for natural language interactions and explanations.

---

## 🎯 Problem Statement

Indian students face challenges in career decision-making:
- Limited access to personalized career guidance
- Overwhelming number of career options
- Lack of transparency in recommendation systems
- Need for context-aware advice (Indian education system, job market, locations)

## 💡 Solution

A production-ready, AWS-native serverless system that:
1. **Engages naturally** using AWS Bedrock for dynamic AI conversations
2. **Ranks careers** using explainable ML with transparent scoring
3. **Explains recommendations** with AWS Bedrock-powered personalized roadmaps
4. **Respects privacy** with consent-first, session-only data storage
5. **Scales automatically** using AWS Lambda, API Gateway, and DynamoDB

---

## 🏗️ Architecture

### AWS Services Used

- **AWS Bedrock** - Claude 3 Sonnet for AI conversations and explanations
- **AWS Lambda** - Serverless compute for API logic
- **Amazon API Gateway** - RESTful API endpoints
- **Amazon S3** - Career dataset storage and static website hosting
- **Amazon DynamoDB** - Session management (24-hour TTL)
- **Amazon CloudFront** - Global CDN for frontend delivery
- **AWS IAM** - Security and access control

### System Flow

```
User → CloudFront → API Gateway → Lambda → {
  ├─ AWS Bedrock (AI Chat & Explanations)
  ├─ ML Ranking Engine (Explainable Scoring)
  └─ DynamoDB (Session Storage)
} → S3 (Career Data)
```

### Key Design Principles

1. **Separation of Concerns**: ML ranks, AI explains (never decides)
2. **Explainability**: Transparent scoring with breakdown
3. **Privacy-First**: Consent before data collection, session-only storage
4. **Serverless**: Auto-scaling, pay-per-use, zero server management
5. **Indian Context**: Education system, cities, INR salaries, local job market

---

## ✨ Features

### 1. AI-Powered Conversations (AWS Bedrock)
- Natural language understanding
- Context-aware responses
- Answers any career-related question dynamically
- Example: "Is BTech worth it in 2026?" gets intelligent, nuanced responses

### 2. Explainable ML Career Ranking
- Transparent weighted scoring:
  - Skill Match (35%)
  - Education Fit (25%)
  - Interest Alignment (25%)
  - Regional Demand (15%)
- Visual score breakdown
- Top 3 career recommendations

### 3. Personalized Explanations (AWS Bedrock)
- AI-generated career fit analysis
- 5-step roadmap specific to India
- Key strengths identification
- Important considerations

### 4. Ethical AI Implementation
- Explicit user consent before data collection
- No permanent storage without permission
- Transparent methodology
- No guarantees or forced decisions

### 5. Indian Context Awareness
- Education levels (10th, 12th, BTech, MBA, etc.)
- Major cities (Bangalore, Mumbai, Delhi, etc.)
- Salary ranges in INR
- Regional job market demand

---

## 🚀 Quick Start

### Prerequisites
- AWS Account with Bedrock access
- Python 3.11+
- Node.js 18+
- AWS CLI configured

### Local Development

```bash
# 1. Install dependencies
pip install -r backend/requirements.txt
cd frontend && npm install

# 2. Configure AWS credentials
aws configure

# 3. Enable AWS Bedrock access (Claude 3 Sonnet)
# Go to AWS Console → Bedrock → Model access → Enable Claude

# 4. Start backend
python local_server.py

# 5. Start frontend (new terminal)
cd frontend && npm start
```

### AWS Deployment

```bash
# Deploy infrastructure
cd infrastructure
bash deploy.sh

# Or follow manual steps in DEPLOYMENT_GUIDE.md
```

---

## 📊 Demo & Testing

### Test AI Chat
```bash
# Ask any career question
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Is BTech worth it in 2026?", "session_id": "demo"}'
```

### Test Career Ranking
```bash
curl -X POST http://localhost:5000/api/rank-careers \
  -H "Content-Type: application/json" \
  -d '{
    "education": "btech",
    "skills": ["python", "java"],
    "interests": ["technology"],
    "location": "bangalore"
  }'
```

### Sample Output
```json
{
  "careers": [
    {
      "title": "Software Engineer",
      "score": 0.82,
      "breakdown": {
        "skill_match": 0.75,
        "education_fit": 1.0,
        "interest_alignment": 0.67,
        "regional_demand": 0.95
      },
      "metadata": {
        "avg_salary_range": "₹4-15 LPA",
        "growth_outlook": "Excellent"
      }
    }
  ]
}
```

---

## 📁 Project Structure

```
career-guidance-system/
├── backend/                    # Lambda functions
│   ├── ai_chat/               # AWS Bedrock integration
│   │   └── bedrock_chat.py    # AI conversation engine
│   ├── career_ranking/        # ML ranking engine
│   │   └── ranker.py          # Explainable scoring
│   ├── intent_detection/      # Intent classifier
│   │   └── detector.py        # Pattern matching
│   ├── llm_explanation/       # Career explanations
│   │   └── explainer.py       # Bedrock prompts
│   ├── main.py                # Lambda handler
│   └── requirements.txt       # Python dependencies
├── frontend/                   # React application
│   ├── src/
│   │   ├── components/        # UI components
│   │   ├── App.js            # Main app
│   │   └── App.css           # Styles
│   └── package.json          # Node dependencies
├── data/
│   └── careers.json          # Career database (10 careers)
├── infrastructure/            # AWS deployment
│   ├── deploy.sh             # Deployment script
│   ├── lambda-iam-policy.json
│   └── lambda-trust-policy.json
├── tests/                     # Unit tests
│   ├── test_ranker.py
│   └── test_intent_detector.py
├── local_server.py           # Local development server
├── README.md                 # This file
├── ARCHITECTURE.md           # Detailed architecture
├── DEPLOYMENT_GUIDE.md       # AWS deployment steps
├── AWS_BEDROCK_SETUP.md      # Bedrock configuration
└── ETHICS_AND_COMPLIANCE.md  # AI ethics guidelines
```

---

## 🔒 Security & Privacy

### Data Protection
- No permanent storage without explicit consent
- Session data expires after 24 hours
- HTTPS-only communication
- IAM role-based access control
- No PII in logs

### Ethical AI
- Transparent scoring methodology
- Explainable recommendations
- No black-box decisions
- User autonomy (can exit anytime)
- No guarantees or forced choices

---

## 💰 Cost Estimation

### Monthly Costs (1000 users)
- AWS Lambda: ~$5
- API Gateway: ~$3.50
- DynamoDB: ~$1
- S3: ~$0.50
- AWS Bedrock: ~$10-50 (usage-based)
- CloudFront: ~$1

**Total: ~$21-71/month** (very cost-effective!)

---

## 🎯 AWS Bedrock Integration Highlights

### Why AWS Bedrock?
1. **Managed Service**: No infrastructure to manage
2. **Enterprise-Ready**: Built-in security and compliance
3. **Cost-Effective**: Pay only for what you use
4. **High Quality**: Claude 3 Sonnet for intelligent responses
5. **Scalable**: Handles any load automatically

### Use Cases in This Project
1. **Dynamic Conversations**: Natural career guidance chat
2. **Personalized Explanations**: Career fit analysis
3. **Roadmap Generation**: Step-by-step career paths
4. **Context Understanding**: Remembers conversation history

### Prompt Engineering
- System prompts for Indian context
- Structured output for consistency
- Temperature tuning for reliability
- Token limits for cost control

---

## 🏆 Innovation & Impact

### Technical Innovation
- **Hybrid AI**: Combines ML ranking with LLM explanations
- **Explainable AI**: Transparent scoring, not black-box
- **Serverless-First**: Zero server management
- **Privacy-Preserving**: Session-only data storage

### Social Impact
- **Accessibility**: Free career guidance for all Indian students
- **Scalability**: Can serve millions of students
- **Localization**: Indian education system and job market
- **Empowerment**: Informed career decisions

### AWS Best Practices
- ✅ Serverless architecture
- ✅ Managed AI services (Bedrock)
- ✅ Infrastructure as Code
- ✅ Security by design
- ✅ Cost optimization
- ✅ Auto-scaling

---

## 📚 Documentation

- **ARCHITECTURE.md** - Detailed system design
- **DEPLOYMENT_GUIDE.md** - Step-by-step AWS deployment
- **AWS_BEDROCK_SETUP.md** - Bedrock configuration guide
- **ETHICS_AND_COMPLIANCE.md** - AI ethics and privacy
- **SAMPLE_PROMPTS.md** - Bedrock prompt templates
- **PROJECT_STRUCTURE.md** - File organization

---

## 🧪 Testing

```bash
# Run unit tests
python tests/test_ranker.py
python tests/test_intent_detector.py

# Test API endpoints
curl http://localhost:5000/api/health
```

---

## 🚀 Future Enhancements

1. **Multi-language Support** (Hindi, Tamil, Telugu, etc.)
2. **Voice Interface** (Amazon Polly integration)
3. **Career Comparison Tool**
4. **Skill Gap Analysis**
5. **Job Market Trends** (real-time data)
6. **Mentor Matching**
7. **Mobile App** (React Native)

---

## 👥 Team

- **Developer**: [Your Name]
- **Project**: AI for Bharat - Career Guidance System
- **Hackathon**: AWS Hackathon 2026

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- AWS Bedrock team for Claude 3 Sonnet
- Indian students for inspiration
- AWS for serverless infrastructure
- Open source community

---

## 📞 Contact

For questions or demo requests:
- Email: [your-email]
- GitHub: [your-github]
- LinkedIn: [your-linkedin]

---

## 🎉 Conclusion

This project demonstrates how AWS services (especially Bedrock) can be combined with explainable ML to create an ethical, scalable, and impactful AI solution for Indian students. The system is production-ready, cost-effective, and follows AWS best practices.

**Built with ❤️ for Indian Students using AWS**
