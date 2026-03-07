# System Architecture

## Overview
AI-Based Career Guidance System for Indian Students using AWS serverless architecture.

## Architecture Diagram (Text-Based)

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  React Frontend (S3 + CloudFront)                        │  │
│  │  - Chat Interface                                        │  │
│  │  - Career Preference Form                                │  │
│  │  - Results Display with Explanations                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY (REST)                         │
│  Routes: /api/detect-intent                                     │
│          /api/rank-careers                                      │
│          /api/explain-career                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AWS LAMBDA (Python 3.11)                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  1. INTENT DETECTION MODULE                              │  │
│  │     - Rule-based NLP classifier                          │  │
│  │     - Detects: exploration vs personalized guidance      │  │
│  │     - Triggers consent flow if needed                    │  │
│  │     - NO personal data collection before consent         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  2. CAREER RANKING ENGINE (ML)                           │  │
│  │     - Explainable weighted scoring model                 │  │
│  │     - Inputs: education, skills, interests, location     │  │
│  │     - Scoring components:                                │  │
│  │       * Skill Match (35%)                                │  │
│  │       * Education Fit (25%)                              │  │
│  │       * Interest Alignment (25%)                         │  │
│  │       * Regional Demand (15%)                            │  │
│  │     - Output: Top 3 careers with score breakdown         │  │
│  │     - DECISION-MAKING LAYER                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  3. LLM EXPLANATION LAYER (AWS Bedrock)                  │  │
│  │     - Uses Claude 3 Sonnet                               │  │
│  │     - Generates:                                         │  │
│  │       * Why career fits user profile                     │  │
│  │       * Personalized roadmap                             │  │
│  │       * Key strengths analysis                           │  │
│  │     - Prompt templates with strict constraints           │  │
│  │     - LLM NEVER makes decisions, only explains           │  │
│  │     - EXPLANATION-ONLY LAYER                             │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                               │
│  ┌────────────────────┐  ┌────────────────────────────────┐    │
│  │  Amazon S3         │  │  DynamoDB                      │    │
│  │  - careers.json    │  │  - User sessions (24h TTL)     │    │
│  │  - Career docs     │  │  - Temporary storage only      │    │
│  │  - Static assets   │  │  - No permanent user data      │    │
│  └────────────────────┘  └────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Key Design Principles

### 1. Separation of Concerns
- **ML Ranking Engine**: Makes decisions based on data
- **LLM Explanation Layer**: Only explains decisions, never makes them
- Clear boundary prevents LLM hallucinations from affecting recommendations

### 2. Consent-First Architecture
- Intent detection happens BEFORE personal data collection
- Explicit user consent required for personalized recommendations
- Session-based storage with automatic expiration

### 3. Explainability
- Every recommendation includes transparent score breakdown
- Users see exactly why each career was recommended
- Weighted scoring model is tunable and auditable

### 4. Indian Context Awareness
- Education system aligned (10th, 12th, B.Tech, etc.)
- Location-based demand scoring
- Salary ranges in INR
- Career paths relevant to Indian job market

## Data Flow

1. **User Entry** → Chat interface or direct form access
2. **Intent Detection** → Classify user intent (exploration vs guidance)
3. **Consent Check** → If personalized, request explicit consent
4. **Data Collection** → Structured form for education, skills, interests, location
5. **ML Ranking** → Score all careers, return top 3 with breakdown
6. **LLM Explanation** → Generate personalized explanations for each career
7. **Results Display** → Show rankings, scores, explanations, roadmaps

## Security & Privacy

- No permanent storage of personal data
- Session data expires after 24 hours
- IAM roles with least privilege
- API Gateway throttling and authorization
- HTTPS only communication
- No PII in logs

## Scalability

- Serverless architecture scales automatically
- Lambda concurrent execution handles traffic spikes
- DynamoDB on-demand billing
- CloudFront CDN for global distribution
- S3 for static content delivery

## Cost Optimization

- Pay-per-use Lambda pricing
- DynamoDB on-demand mode
- S3 lifecycle policies for old data
- CloudFront caching reduces origin requests
- Bedrock usage optimized with prompt engineering
