# Deployment Guide

## Prerequisites

1. **AWS Account** with:
   - AWS CLI configured (`aws configure`)
   - Bedrock model access enabled (Claude 3 Sonnet)
   - Sufficient permissions for Lambda, S3, DynamoDB, API Gateway

2. **Local Development**:
   - Python 3.11+
   - Node.js 18+
   - npm or yarn

## Step-by-Step Deployment

### Phase 1: Backend Infrastructure

#### 1.1 Create S3 Bucket for Career Data
```bash
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export BUCKET_NAME="career-guidance-data-${AWS_ACCOUNT_ID}"

aws s3 mb s3://${BUCKET_NAME} --region us-east-1
aws s3 cp data/careers.json s3://${BUCKET_NAME}/careers.json
```

#### 1.2 Create DynamoDB Table
```bash
aws dynamodb create-table \
  --table-name CareerGuidanceSessions \
  --attribute-definitions AttributeName=session_id,AttributeType=S \
  --key-schema AttributeName=session_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

#### 1.3 Create IAM Role for Lambda
```bash
cd infrastructure

# Create role
aws iam create-role \
  --role-name lambda-career-guidance-role \
  --assume-role-policy-document file://lambda-trust-policy.json

# Attach policy
aws iam put-role-policy \
  --role-name lambda-career-guidance-role \
  --policy-name lambda-career-guidance-policy \
  --policy-document file://lambda-iam-policy.json

# Wait for role propagation
sleep 10
```

#### 1.4 Package and Deploy Lambda
```bash
cd ../backend

# Install dependencies
pip install -r requirements.txt -t package/

# Create deployment package
cd package
zip -r ../lambda.zip .
cd ..
zip -g lambda.zip main.py
zip -rg lambda.zip intent_detection/ career_ranking/ llm_explanation/

# Deploy Lambda
aws lambda create-function \
  --function-name career-guidance-api \
  --runtime python3.11 \
  --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/lambda-career-guidance-role \
  --handler main.lambda_handler \
  --zip-file fileb://lambda.zip \
  --timeout 30 \
  --memory-size 512 \
  --environment Variables="{BUCKET_NAME=${BUCKET_NAME}}" \
  --region us-east-1
```

### Phase 2: API Gateway Setup

#### 2.1 Create REST API
```bash
API_ID=$(aws apigateway create-rest-api \
  --name career-guidance-api \
  --region us-east-1 \
  --query 'id' \
  --output text)

echo "API ID: ${API_ID}"
```

#### 2.2 Get Root Resource ID
```bash
ROOT_ID=$(aws apigateway get-resources \
  --rest-api-id ${API_ID} \
  --region us-east-1 \
  --query 'items[0].id' \
  --output text)
```

#### 2.3 Create /api Resource
```bash
API_RESOURCE_ID=$(aws apigateway create-resource \
  --rest-api-id ${API_ID} \
  --parent-id ${ROOT_ID} \
  --path-part api \
  --region us-east-1 \
  --query 'id' \
  --output text)
```

#### 2.4 Create Endpoints
```bash
# Create /api/detect-intent
INTENT_RESOURCE_ID=$(aws apigateway create-resource \
  --rest-api-id ${API_ID} \
  --parent-id ${API_RESOURCE_ID} \
  --path-part detect-intent \
  --region us-east-1 \
  --query 'id' \
  --output text)

aws apigateway put-method \
  --rest-api-id ${API_ID} \
  --resource-id ${INTENT_RESOURCE_ID} \
  --http-method POST \
  --authorization-type NONE \
  --region us-east-1

# Similar steps for /api/rank-careers and /api/explain-career
```

#### 2.5 Deploy API
```bash
aws apigateway create-deployment \
  --rest-api-id ${API_ID} \
  --stage-name prod \
  --region us-east-1

API_URL="https://${API_ID}.execute-api.us-east-1.amazonaws.com/prod"
echo "API URL: ${API_URL}"
```

### Phase 3: Frontend Deployment

#### 3.1 Build Frontend
```bash
cd frontend

# Install dependencies
npm install

# Set API URL
echo "REACT_APP_API_URL=${API_URL}" > .env

# Build
npm run build
```

#### 3.2 Create S3 Bucket for Frontend
```bash
FRONTEND_BUCKET="career-guidance-frontend-${AWS_ACCOUNT_ID}"

aws s3 mb s3://${FRONTEND_BUCKET} --region us-east-1

# Configure for static website hosting
aws s3 website s3://${FRONTEND_BUCKET} \
  --index-document index.html \
  --error-document index.html
```

#### 3.3 Upload Frontend
```bash
aws s3 sync build/ s3://${FRONTEND_BUCKET} --acl public-read
```

#### 3.4 Create CloudFront Distribution
```bash
aws cloudfront create-distribution \
  --origin-domain-name ${FRONTEND_BUCKET}.s3.amazonaws.com \
  --default-root-object index.html
```

## Testing

### Test Intent Detection
```bash
curl -X POST ${API_URL}/api/detect-intent \
  -H "Content-Type: application/json" \
  -d '{"message": "I want career recommendations"}'
```

### Test Career Ranking
```bash
curl -X POST ${API_URL}/api/rank-careers \
  -H "Content-Type: application/json" \
  -d '{
    "education": "btech",
    "skills": ["python", "java"],
    "interests": ["technology", "problem_solving"],
    "location": "bangalore"
  }'
```

## Monitoring

### CloudWatch Logs
```bash
aws logs tail /aws/lambda/career-guidance-api --follow
```

### Lambda Metrics
```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=career-guidance-api \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

## Troubleshooting

### Lambda Timeout
- Increase timeout: `aws lambda update-function-configuration --function-name career-guidance-api --timeout 60`

### Bedrock Access Denied
- Enable Bedrock model access in AWS Console
- Verify IAM permissions include `bedrock:InvokeModel`

### CORS Issues
- Add CORS headers in Lambda response
- Configure API Gateway CORS settings

## Cleanup

```bash
# Delete Lambda
aws lambda delete-function --function-name career-guidance-api

# Delete API Gateway
aws apigateway delete-rest-api --rest-api-id ${API_ID}

# Delete S3 buckets
aws s3 rb s3://${BUCKET_NAME} --force
aws s3 rb s3://${FRONTEND_BUCKET} --force

# Delete DynamoDB table
aws dynamodb delete-table --table-name CareerGuidanceSessions

# Delete IAM role
aws iam delete-role-policy --role-name lambda-career-guidance-role --policy-name lambda-career-guidance-policy
aws iam delete-role --role-name lambda-career-guidance-role
```
