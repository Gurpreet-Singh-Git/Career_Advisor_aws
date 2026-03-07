import React from 'react';

function ResultsDisplay({ results, onStartOver }) {
  const { rankings, explanations } = results;

  return (
    <div className="results-display">
      <h2>Your Top 3 Career Recommendations</h2>
      <p>Based on your profile, here are careers that match your strengths</p>

      {rankings.map((career, index) => {
        const explanation = explanations[index];
        
        return (
          <div key={index} className="career-card">
            <div className="career-header">
              <h3>#{index + 1} {career.title}</h3>
              <div className="career-score">
                Match Score: <strong>{(career.score * 100).toFixed(0)}%</strong>
              </div>
            </div>

            <div className="career-category">
              Category: {career.category}
            </div>

            <div className="score-breakdown">
              <h4>Why this career matches you:</h4>
              <div className="score-bars">
                <div className="score-item">
                  <span>Skill Match (35%)</span>
                  <div className="score-bar">
                    <div 
                      className="score-fill" 
                      style={{width: `${career.breakdown.skill_match * 100}%`}}
                    />
                  </div>
                  <span>{(career.breakdown.skill_match * 100).toFixed(0)}%</span>
                </div>
                <div className="score-item">
                  <span>Education Fit (25%)</span>
                  <div className="score-bar">
                    <div 
                      className="score-fill" 
                      style={{width: `${career.breakdown.education_fit * 100}%`}}
                    />
                  </div>
                  <span>{(career.breakdown.education_fit * 100).toFixed(0)}%</span>
                </div>
                <div className="score-item">
                  <span>Interest Alignment (25%)</span>
                  <div className="score-bar">
                    <div 
                      className="score-fill" 
                      style={{width: `${career.breakdown.interest_alignment * 100}%`}}
                    />
                  </div>
                  <span>{(career.breakdown.interest_alignment * 100).toFixed(0)}%</span>
                </div>
                <div className="score-item">
                  <span>Regional Demand (15%)</span>
                  <div className="score-bar">
                    <div 
                      className="score-fill" 
                      style={{width: `${career.breakdown.regional_demand * 100}%`}}
                    />
                  </div>
                  <span>{(career.breakdown.regional_demand * 100).toFixed(0)}%</span>
                </div>
              </div>
            </div>

            {explanation && (
              <div className="career-explanation">
                <h4>Detailed Analysis:</h4>
                <p>{explanation.explanation}</p>
                
                {explanation.key_strengths && explanation.key_strengths.length > 0 && (
                  <div className="key-strengths">
                    <strong>Your Key Strengths:</strong>
                    <ul>
                      {explanation.key_strengths.map((strength, i) => (
                        <li key={i}>{strength}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {explanation.roadmap && explanation.roadmap.length > 0 && (
                  <div className="roadmap">
                    <strong>Roadmap to Success:</strong>
                    <ol>
                      {explanation.roadmap.map((step, i) => (
                        <li key={i}>{step}</li>
                      ))}
                    </ol>
                  </div>
                )}
              </div>
            )}

            <div className="career-metadata">
              <div>💰 Salary: {career.metadata.avg_salary_range}</div>
              <div>📈 Growth: {career.metadata.growth_outlook}</div>
              <div>🎓 Education: {career.metadata.education_required}</div>
            </div>
          </div>
        );
      })}

      <button onClick={onStartOver} className="start-over-btn">
        Start Over
      </button>

      <div className="disclaimer">
        <p>⚠️ These recommendations are based on data analysis and should be used as guidance, not guarantees. 
        Consider consulting with career counselors and exploring multiple options before making decisions.</p>
      </div>
    </div>
  );
}

export default ResultsDisplay;
