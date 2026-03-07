# Contributing to AI Career Guidance System

Thank you for your interest in contributing! This project aims to provide accessible career guidance to Indian students.

## How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs
- Include detailed description and steps to reproduce
- Attach screenshots if applicable

### Suggesting Features
- Open an issue with [Feature Request] tag
- Describe the feature and its benefits
- Consider Indian student context

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed
4. **Test your changes**
   ```bash
   python tests/test_ranker.py
   python tests/test_intent_detector.py
   ```
5. **Commit with clear message**
   ```bash
   git commit -m "Add: feature description"
   ```
6. **Push and create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Adding Careers

To add new careers to the database:

1. Edit `data/careers.json`
2. Follow this structure:
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
  "min_education": "Minimum education"
}
```

### Code Style

- **Python**: Follow PEP 8
- **JavaScript**: Use ES6+ features
- **Comments**: Explain why, not what
- **Naming**: Descriptive variable names

### Testing

- Write unit tests for new features
- Ensure existing tests pass
- Test with different user profiles

### Documentation

- Update README.md for major changes
- Add docstrings to functions
- Update architecture docs if needed

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Prioritize student welfare

## Questions?

Open an issue or contact the maintainers.

Thank you for contributing! 🙏
