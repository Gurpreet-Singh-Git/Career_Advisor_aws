# Sample Bedrock Prompt Templates

## Career Explanation Prompt Template

This template is used in `backend/llm_explanation/explainer.py` to generate career explanations.

### Key Constraints:
1. LLM explains decisions, never makes them
2. Grounded in ML scoring breakdown
3. Indian education system context
4. Structured JSON output

### Example Prompt:

```
You are a career guidance assistant for Indian students. Your role is to EXPLAIN career recommendations, not make decisions.

IMPORTANT CONSTRAINTS:
- You are explaining a career that has ALREADY been ranked by an ML system
- Do NOT suggest alternative careers or question the ranking
- Focus ONLY on explaining WHY this career fits the user
- Be specific to the Indian education system and job market
- Keep explanations concise (150-200 words)
- Provide actionable roadmap steps

CAREER TO EXPLAIN: Software Engineer

USER PROFILE:
- Education: B.Tech Computer Science
- Skills: Python, Java, Problem Solving
- Interests: Technology, Innovation, Coding
- Location: Bangalore

ML SCORING BREAKDOWN (0.0 to 1.0):
- Skill Match: 0.95 (35% weight)
- Education Fit: 1.0 (25% weight)
- Interest Alignment: 0.90 (25% weight)
- Regional Demand: 0.95 (15% weight)

TASK:
1. Explain WHY this career matches the user's profile based on the scores above
2. Highlight specific connections between user's skills/interests and career requirements
3. Provide a 5-step roadmap specific to Indian context

FORMAT YOUR RESPONSE AS JSON:
{
  "explanation": "Your explanation here...",
  "key_strengths": ["strength 1", "strength 2", "strength 3"],
  "roadmap": [
    "Step 1: ...",
    "Step 2: ...",
    "Step 3: ...",
    "Step 4: ...",
    "Step 5: ..."
  ],
  "considerations": "Any important considerations or challenges..."
}
```

### Expected Output:

```json
{
  "explanation": "Software Engineering is an excellent match for your profile. With your B.Tech in Computer Science and strong skills in Python and Java, you have the exact technical foundation this career demands. Your 95% skill match score reflects how well your programming abilities align with industry requirements. Bangalore, your location, is India's tech capital with the highest demand for software engineers (95% regional score), offering abundant opportunities in startups and MNCs alike.",
  "key_strengths": [
    "Strong programming foundation in Python and Java",
    "B.Tech CS degree perfectly aligns with industry requirements",
    "Located in Bangalore - India's premier tech hub",
    "Natural interest in technology and innovation"
  ],
  "roadmap": [
    "Step 1: Master data structures and algorithms through platforms like LeetCode and GeeksforGeeks",
    "Step 2: Build 3-4 substantial projects showcasing full-stack development skills",
    "Step 3: Contribute to open-source projects on GitHub to build portfolio",
    "Step 4: Apply for internships at tech companies in Bangalore (Flipkart, Amazon, startups)",
    "Step 5: Prepare for technical interviews and apply to product-based companies"
  ],
  "considerations": "The tech industry is competitive. Focus on continuous learning, stay updated with latest frameworks, and build a strong GitHub profile. Consider specializing in areas like cloud computing, AI/ML, or mobile development to stand out."
}
```

## Prompt Engineering Best Practices

### 1. Constraint-First Design
Always start with what the LLM should NOT do:
- Don't make decisions
- Don't suggest alternatives
- Don't question the ML ranking

### 2. Context Grounding
Provide explicit context:
- User profile details
- ML scoring breakdown with weights
- Geographic and cultural context (Indian market)

### 3. Structured Output
Request JSON format for:
- Consistent parsing
- Type safety
- Easy integration with frontend

### 4. Indian Context Specificity
Include references to:
- Indian education system (10th, 12th, B.Tech, etc.)
- Indian cities and job markets
- Salary ranges in INR
- Local career platforms (Naukri, LinkedIn India)

### 5. Actionable Guidance
Roadmap should include:
- Specific Indian platforms (GeeksforGeeks, NPTEL)
- Local opportunities (internships, companies)
- Realistic timelines
- Certification paths (NPTEL, Coursera India)

## Alternative Models

### Using AWS Titan
```python
model_id = 'amazon.titan-text-express-v1'

request_body = {
    "inputText": prompt,
    "textGenerationConfig": {
        "maxTokenCount": 1000,
        "temperature": 0.7,
        "topP": 0.9
    }
}
```

### Using Claude 3 Haiku (Faster, Cheaper)
```python
model_id = 'anthropic.claude-3-haiku-20240307-v1:0'
# Same request format as Sonnet
```

## Cost Optimization

1. **Prompt Caching**: Reuse system instructions across requests
2. **Token Limits**: Set max_tokens to prevent overuse
3. **Batch Processing**: Generate multiple explanations in one call
4. **Fallback Templates**: Use template-based responses when Bedrock unavailable

## Testing Prompts

Test with diverse profiles:
- Different education levels (12th, Diploma, B.Tech, MBA)
- Various locations (Tier 1, Tier 2, Tier 3 cities)
- Multiple skill combinations
- Edge cases (low scores, conflicting interests)
