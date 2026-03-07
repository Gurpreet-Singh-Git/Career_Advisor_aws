# Ethics and Compliance Guidelines

## Ethical AI Principles

### 1. Consent-First Approach
- **No data collection without explicit consent**
- Intent detection happens before any personal information is requested
- Users must actively agree to share their profile information
- Clear explanation of how data will be used

### 2. Transparency
- **Explainable scoring methodology**
  - Each recommendation includes score breakdown
  - Weights are visible and documented
  - Users understand why careers were recommended
- **No black-box decisions**
  - ML model uses interpretable weighted scoring
  - LLM only explains, never decides

### 3. User Autonomy
- **No guarantees or forced decisions**
  - Recommendations are guidance, not prescriptions
  - Users can exit at any time
  - Multiple options provided (top 3)
- **Right to be forgotten**
  - Session data expires after 24 hours
  - No permanent storage without consent

### 4. Fairness and Bias Mitigation
- **Regional fairness**
  - Scoring considers local job market conditions
  - No bias toward metro cities
  - Tier 2/3 cities represented in demand data
- **Education accessibility**
  - Multiple education paths for each career
  - No discrimination based on education level
  - Diploma and 12th pass options included

### 5. Privacy Protection
- **Minimal data collection**
  - Only essential information requested
  - No PII beyond session requirements
  - No tracking or profiling
- **Data security**
  - HTTPS only communication
  - IAM role-based access control
  - No logs containing personal data

## Compliance Requirements

### Data Protection
- **GDPR-inspired principles** (though India-focused)
  - Right to access
  - Right to deletion
  - Data minimization
  - Purpose limitation

### Indian Context
- **No caste/religion/gender discrimination**
  - Scoring is merit and interest-based only
  - No demographic profiling
  - Equal opportunity recommendations

### Disclaimers
Required disclaimers shown to users:
1. "These are recommendations, not guarantees"
2. "Consult with career counselors before making decisions"
3. "Your data is used only for this session"
4. "You can exit anytime"

## LLM Safety Constraints

### Prompt Engineering for Safety
1. **Strict role definition**
   - LLM is an explainer, not a decision-maker
   - Cannot suggest alternative careers
   - Cannot question ML rankings

2. **Grounding in facts**
   - All explanations based on ML scores
   - No hallucinated career information
   - Indian job market context enforced

3. **Avoiding harmful content**
   - No guarantees of success
   - No unrealistic expectations
   - Balanced view of challenges

### Fallback Mechanisms
- Template-based responses if Bedrock fails
- Error handling for API failures
- Graceful degradation

## Monitoring and Auditing

### Metrics to Track
1. **Fairness metrics**
   - Distribution of recommendations by education level
   - Geographic distribution of users
   - Career category diversity

2. **Quality metrics**
   - User satisfaction (if feedback collected)
   - Recommendation relevance
   - LLM explanation quality

3. **Safety metrics**
   - Consent acceptance rate
   - Session duration
   - Exit points

### Regular Audits
- Review career dataset for bias
- Validate scoring weights
- Test LLM prompts for safety
- Check compliance with privacy policies

## Responsible AI Checklist

- [ ] Explicit user consent obtained
- [ ] Transparent scoring methodology
- [ ] No permanent data storage without consent
- [ ] Multiple career options provided
- [ ] Disclaimers clearly displayed
- [ ] LLM constrained to explanation only
- [ ] Regional fairness considered
- [ ] Education accessibility ensured
- [ ] Privacy protections implemented
- [ ] Bias mitigation strategies applied

## Incident Response

### If Bias Detected
1. Pause recommendations
2. Audit career dataset
3. Review scoring weights
4. Test with diverse profiles
5. Update and redeploy

### If Privacy Breach
1. Identify scope
2. Notify affected users
3. Patch vulnerability
4. Review access logs
5. Update security policies

### If LLM Misbehavior
1. Review prompt templates
2. Add stricter constraints
3. Implement content filtering
4. Test with edge cases
5. Update fallback mechanisms

## Future Enhancements

### Planned Improvements
1. **Bias detection dashboard**
   - Real-time fairness monitoring
   - Demographic distribution analysis
   - Alert system for anomalies

2. **User feedback loop**
   - Optional satisfaction surveys
   - Recommendation quality tracking
   - Continuous improvement

3. **Accessibility features**
   - Multi-language support (Hindi, Tamil, etc.)
   - Screen reader compatibility
   - Simple language mode

4. **Enhanced transparency**
   - Interactive score explanation
   - "Why not other careers?" feature
   - Career comparison tool

## References

- [AI Ethics Guidelines - NITI Aayog](https://www.niti.gov.in/)
- [Responsible AI Practices - Google](https://ai.google/responsibility/responsible-ai-practices/)
- [AWS Responsible AI](https://aws.amazon.com/machine-learning/responsible-ai/)
- [Digital Personal Data Protection Act, 2023 (India)](https://www.meity.gov.in/)
