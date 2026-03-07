# Project Structure

```
career-guidance-system/
│
├── README.md                          # Project overview and quick start
├── ARCHITECTURE.md                    # Detailed architecture documentation
├── DEPLOYMENT_GUIDE.md                # Step-by-step deployment instructions
├── SAMPLE_PROMPTS.md                  # Bedrock prompt templates and examples
├── PROJECT_STRUCTURE.md               # This file
├── .gitignore                         # Git ignore rules
│
├── backend/                           # Lambda function code
│   ├── main.py                        # Main Lambda handler (API router)
│   ├── requirements.txt               # Python dependencies
│   │
│   ├── intent_detection/              # Module 1: Intent Detection
│   │   └── detector.py                # Rule-based NLP classifier
│   │
│   ├── career_ranking/                # Module 2: ML Ranking Engine
│   │   └── ranker.py                  # Explainable scoring model
│   │
│   └── llm_explanation/               # Module 3: LLM Explanation Layer
│       └── explainer.py               # AWS Bedrock integration
│
├── frontend/                          # React web application
│   ├── package.json                   # Node dependencies
│   ├── public/
│   │   └── index.html                 # HTML template
│   │
│   └── src/
│       ├── index.js                   # React entry point
│       ├── App.js                     # Main application component
│       ├── App.css                    # Global styles
│       │
│       └── components/
│           ├── ChatInterface.js       # Chat-style entry interface
│           ├── CareerForm.js          # Structured preference form
│           └── ResultsDisplay.js      # Career recommendations display
│
├── data/                              # Career datasets
│   └── careers.json                   # Career information database
│
├── infrastructure/                    # AWS deployment configs
│   ├── deploy.sh                      # Automated deployment script
│   ├── lambda-iam-policy.json         # IAM permissions for Lambda
│   └── lambda-trust-policy.json       # Lambda execution role trust policy
│
└── tests/                             # Unit tests
    ├── test_ranker.py                 # Tests for ranking engine
    └── test_intent_detector.py        # Tests for intent detection
```

## Module Descriptions

### Backend Modules

#### 1. Intent Detection (`intent_detection/detector.py`)
- **Purpose**: Classify user intent before collecting personal data
- **Method**: Rule-based pattern matching
- **Outputs**: 
  - Intent type (exploration/personalized_guidance/information_query)
  - Consent requirement flag
  - Appropriate response message

#### 2. Career Ranking Engine (`career_ranking/ranker.py`)
- **Purpose**: Score and rank careers based on user profile
- **Method**: Explainable weighted scoring
- **Inputs**: Education, skills, interests, location
- **Outputs**: Top 3 careers with score breakdown
- **Key Feature**: Transparent, auditable decision-making

#### 3. LLM Explanation Layer (`llm_explanation/explainer.py`)
- **Purpose**: Generate human-readable explanations
- **Method**: AWS Bedrock (Claude 3 Sonnet)
- **Constraint**: Explains decisions, never makes them
- **Outputs**: Explanation, key strengths, roadmap

### Frontend Components

#### 1. ChatInterface
- Natural language entry point
- Quick action buttons
- Intent-aware conversation flow

#### 2. CareerForm
- Structured data collection
- Tag-based skill/interest input
- Education level dropdown
- Location input

#### 3. ResultsDisplay
- Top 3 career cards
- Visual score breakdown
- LLM-generated explanations
- Personalized roadmaps
- Salary and growth information

### Data Layer

#### careers.json Structure
```json
{
  "title": "Career Title",
  "category": "Category",
  "required_skills": ["skill1", "skill2"],
  "education_paths": ["education1", "education2"],
  "related_interests": ["interest1", "interest2"],
  "demand_by_region": {
    "city": 0.0-1.0
  },
  "salary_range": "₹X-Y LPA",
  "growth_outlook": "Excellent/Good/Moderate",
  "min_education": "Minimum education required"
}
```

## Key Files

### Configuration Files
- `backend/requirements.txt`: Python dependencies (boto3, scikit-learn)
- `frontend/package.json`: React dependencies
- `infrastructure/lambda-iam-policy.json`: AWS permissions

### Deployment Files
- `infrastructure/deploy.sh`: Automated deployment script
- `DEPLOYMENT_GUIDE.md`: Manual deployment steps

### Documentation Files
- `README.md`: Quick start and overview
- `ARCHITECTURE.md`: System design and principles
- `SAMPLE_PROMPTS.md`: LLM prompt engineering guide

## Data Flow Through Modules

1. **User Input** → `ChatInterface.js`
2. **Intent Detection** → `detector.py` → Consent check
3. **Form Submission** → `CareerForm.js` → API Gateway
4. **Career Ranking** → `ranker.py` → Top 3 careers with scores
5. **LLM Explanation** → `explainer.py` → Bedrock → Explanations
6. **Results Display** → `ResultsDisplay.js` → User sees recommendations

## AWS Resources Created

- **Lambda Function**: `career-guidance-api`
- **API Gateway**: REST API with 3 endpoints
- **S3 Buckets**: 
  - `career-guidance-data-{account-id}` (career data)
  - `career-guidance-frontend-{account-id}` (static website)
- **DynamoDB Table**: `CareerGuidanceSessions`
- **IAM Role**: `lambda-career-guidance-role`
- **CloudFront Distribution**: CDN for frontend

## Environment Variables

### Backend (Lambda)
- `BUCKET_NAME`: S3 bucket for career data
- `AWS_REGION`: AWS region (default: us-east-1)

### Frontend (React)
- `REACT_APP_API_URL`: API Gateway endpoint URL

## Testing

Run unit tests:
```bash
cd tests
python test_ranker.py
python test_intent_detector.py
```

## Adding New Careers

1. Edit `data/careers.json`
2. Follow the JSON structure
3. Upload to S3: `aws s3 cp data/careers.json s3://${BUCKET_NAME}/`
4. No code changes needed - data-driven design
