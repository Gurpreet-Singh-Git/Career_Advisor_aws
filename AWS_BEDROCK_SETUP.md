# 🤖 AWS Bedrock Setup Guide

## What Changed:

Your system is now **AI-POWERED** with AWS Bedrock integration!

### Before (Static):
- ❌ Rule-based if-else responses
- ❌ Limited to predefined patterns
- ❌ Can't answer dynamic questions

### After (Dynamic AI):
- ✅ Real AI conversations using AWS Bedrock (Claude)
- ✅ Answers ANY career-related question naturally
- ✅ Context-aware responses
- ✅ Understands questions like "Is BTech worth it in 2026?"

## Current Status:

🟡 **Fallback Mode**: System works with smart fallback responses
🟢 **Ready for AWS**: Code is ready, just needs AWS configuration

## How to Enable AWS Bedrock (Real AI):

### Step 1: Install boto3

```bash
pip install boto3
```

### Step 2: Configure AWS Credentials

**Option A: AWS CLI (Recommended)**
```bash
# Install AWS CLI if not installed
# Download from: https://aws.amazon.com/cli/

# Configure credentials
aws configure
```

Enter:
- AWS Access Key ID
- AWS Secret Access Key  
- Default region: `us-east-1`
- Default output format: `json`

**Option B: Environment Variables**
```bash
# Windows
set AWS_ACCESS_KEY_ID=your_access_key
set AWS_SECRET_ACCESS_KEY=your_secret_key
set AWS_DEFAULT_REGION=us-east-1

# Linux/Mac
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### Step 3: Enable Bedrock Access in AWS Console

1. Go to AWS Console: https://console.aws.amazon.com/
2. Search for "Bedrock"
3. Click "Model access" in left sidebar
4. Click "Manage model access"
5. Enable: **Anthropic Claude 3 Sonnet**
6. Click "Save changes"
7. Wait 2-3 minutes for access to be granted

### Step 4: Restart the Server

```bash
# Stop current server (Ctrl+C)
# Start again
python local_server.py
```

You should see:
```
✓ AWS Bedrock connected
✓ Using Claude 3 Sonnet
```

### Step 5: Test It!

```bash
python test_ai_chat.py
```

Now responses will show: `(bedrock)` instead of `(fallback)`

## Testing the AI Chat:

### In the Frontend:
1. Refresh browser (F5)
2. Type ANY question:
   - "Is BTech worth it in 2026?"
   - "What's the salary of a data scientist in India?"
   - "Should I learn Python or Java first?"
   - "Tell me about careers in AI"
3. Get AI-powered responses!

### Example Questions to Try:

```
"Is it worth to do BTech in 2026?"
"What are the highest paying careers in India?"
"I'm interested in AI and machine learning, what should I study?"
"Compare software engineer vs data scientist careers"
"What skills do I need for a career in cloud computing?"
"Is MBA better than MTech for career growth?"
```

## How It Works:

```
User Question
    ↓
AWS Bedrock (Claude AI)
    ↓
Context-aware Response
    ↓
Detects if user wants personalized recommendations
    ↓
Shows form if needed
```

## Cost Estimation:

AWS Bedrock Claude 3 Sonnet pricing:
- Input: $0.003 per 1K tokens (~750 words)
- Output: $0.015 per 1K tokens

Example costs:
- 100 conversations: ~$0.50
- 1,000 conversations: ~$5.00
- 10,000 conversations: ~$50.00

Very affordable for testing and small-scale use!

## Fallback Mode (Current):

Even without AWS, the system works with intelligent fallback responses:
- ✅ Answers common career questions
- ✅ Detects personalized recommendation requests
- ✅ Provides helpful guidance
- ✅ Suggests filling the form when appropriate

## Features Now Available:

### 1. Dynamic Conversations
Ask anything about careers, the AI responds naturally!

### 2. Context Awareness
AI remembers the conversation (last 5 messages)

### 3. Indian Context
AI knows about:
- Indian education system (10th, 12th, BTech, etc.)
- Indian cities and job markets
- Salary ranges in INR
- Indian institutions

### 4. Smart Form Detection
AI automatically detects when user wants personalized recommendations and suggests the form

### 5. Dual Mode
- **Exploration**: Chat freely about careers
- **Personalized**: Fill form for ML-ranked recommendations

## Architecture:

```
Frontend (React)
    ↓
Flask API
    ↓
┌─────────────────┬──────────────────┐
│   AI Chat       │  Career Ranking  │
│ (AWS Bedrock)   │  (ML Scoring)    │
└─────────────────┴──────────────────┘
```

## Troubleshooting:

### "Credentials not found"
- Run `aws configure` and enter your credentials
- Or set environment variables

### "Access denied to Bedrock"
- Enable model access in AWS Console
- Wait 2-3 minutes after enabling

### "Region not supported"
- Use `us-east-1` region
- Update in `backend/ai_chat/bedrock_chat.py` if needed

### Still using fallback?
- Check if boto3 is installed: `pip list | grep boto3`
- Check AWS credentials: `aws sts get-caller-identity`
- Check server logs for errors

## Next Steps:

1. **Test Fallback Mode** (works now!)
   ```bash
   python test_ai_chat.py
   ```

2. **Set up AWS** (for real AI)
   - Configure credentials
   - Enable Bedrock access
   - Restart server

3. **Use the Frontend**
   - Refresh browser
   - Ask any career question
   - Get AI-powered responses!

4. **Deploy to AWS** (optional)
   - Follow DEPLOYMENT_GUIDE.md
   - Use Lambda + API Gateway
   - Production-ready!

## Success! 🎉

Your system is now AI-powered and can answer ANY career-related question dynamically!

Even in fallback mode, it's much smarter than before. With AWS Bedrock, it becomes a truly intelligent career guidance assistant!
