#!/bin/bash
# Deployment script for Career Guidance System

set -e

AWS_REGION="us-east-1"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET_NAME="career-guidance-data-${AWS_ACCOUNT_ID}"
LAMBDA_FUNCTION_NAME="career-guidance-api"

echo "Deploying Career Guidance System..."
echo "AWS Account: ${AWS_ACCOUNT_ID}"
echo "Region: ${AWS_REGION}"

# Step 1: Create S3 bucket for career data
echo "Creating S3 bucket..."
aws s3 mb s3://${BUCKET_NAME} --region ${AWS_REGION} || echo "Bucket already exists"
aws s3 cp ../data/careers.json s3://${BUCKET_NAME}/careers.json

# Step 2: Create DynamoDB table
echo "Creating DynamoDB table..."
aws dynamodb create-table \
  --table-name CareerGuidanceSessions \
  --attribute-definitions AttributeName=session_id,AttributeType=S \
  --key-schema AttributeName=session_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region ${AWS_REGION} || echo "Table already exists"

# Step 3: Create IAM role for Lambda
echo "Creating IAM role..."
aws iam create-role \
  --role-name lambda-career-guidance-role \
  --assume-role-policy-document file://lambda-trust-policy.json || echo "Role exists"

aws iam put-role-policy \
  --role-name lambda-career-guidance-role \
  --policy-name lambda-career-guidance-policy \
  --policy-document file://lambda-iam-policy.json

# Step 4: Package and deploy Lambda
echo "Packaging Lambda function..."
cd ../backend
pip install -r requirements.txt -t package/
cd package && zip -r ../lambda.zip . && cd ..
zip -g lambda.zip main.py
zip -rg lambda.zip intent_detection/ career_ranking/ llm_explanation/

echo "Deploying Lambda function..."
aws lambda create-function \
  --function-name ${LAMBDA_FUNCTION_NAME} \
  --runtime python3.11 \
  --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/lambda-career-guidance-role \
  --handler main.lambda_handler \
  --zip-file fileb://lambda.zip \
  --timeout 30 \
  --memory-size 512 \
  --region ${AWS_REGION} || \
aws lambda update-function-code \
  --function-name ${LAMBDA_FUNCTION_NAME} \
  --zip-file fileb://lambda.zip \
  --region ${AWS_REGION}

echo "Deployment complete!"
echo "Next steps:"
echo "1. Configure API Gateway"
echo "2. Deploy frontend to S3"
echo "3. Set up CloudFront distribution"
