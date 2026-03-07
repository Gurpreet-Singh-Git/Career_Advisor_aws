import React, { useState } from 'react';

function CareerForm({ onSubmit, onBack }) {
  const [formData, setFormData] = useState({
    education: '',
    skills: [],
    interests: [],
    location: ''
  });

  const [skillInput, setSkillInput] = useState('');
  const [interestInput, setInterestInput] = useState('');

  const educationOptions = [
    { value: '10th', label: '10th Standard' },
    { value: '12th_science', label: '12th Science' },
    { value: '12th_commerce', label: '12th Commerce' },
    { value: '12th_arts', label: '12th Arts' },
    { value: 'diploma', label: 'Diploma' },
    { value: 'btech', label: 'B.Tech/B.E.' },
    { value: 'bsc', label: 'B.Sc' },
    { value: 'bcom', label: 'B.Com' },
    { value: 'ba', label: 'B.A.' },
    { value: 'mtech', label: 'M.Tech' },
    { value: 'mba', label: 'MBA' }
  ];

  const handleAddSkill = () => {
    if (skillInput.trim() && !formData.skills.includes(skillInput.trim())) {
      setFormData({
        ...formData,
        skills: [...formData.skills, skillInput.trim()]
      });
      setSkillInput('');
    }
  };

  const handleAddInterest = () => {
    if (interestInput.trim() && !formData.interests.includes(interestInput.trim())) {
      setFormData({
        ...formData,
        interests: [...formData.interests, interestInput.trim()]
      });
      setInterestInput('');
    }
  };

  const handleRemoveSkill = (skill) => {
    setFormData({
      ...formData,
      skills: formData.skills.filter(s => s !== skill)
    });
  };

  const handleRemoveInterest = (interest) => {
    setFormData({
      ...formData,
      interests: formData.interests.filter(i => i !== interest)
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.education && formData.skills.length > 0 && 
        formData.interests.length > 0 && formData.location) {
      onSubmit(formData);
    } else {
      alert('Please fill all fields');
    }
  };

  return (
    <div className="career-form">
      <button onClick={onBack} className="back-btn">← Back</button>
      
      <h2>Tell us about yourself</h2>
      <p>This information helps us provide personalized recommendations</p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Education Level *</label>
          <select 
            value={formData.education}
            onChange={(e) => setFormData({...formData, education: e.target.value})}
            required
          >
            <option value="">Select your education level</option>
            {educationOptions.map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Skills *</label>
          <div className="tag-input">
            <input
              type="text"
              value={skillInput}
              onChange={(e) => setSkillInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddSkill())}
              placeholder="e.g., Python, Communication, Design"
            />
            <button type="button" onClick={handleAddSkill}>Add</button>
          </div>
          <div className="tags">
            {formData.skills.map(skill => (
              <span key={skill} className="tag">
                {skill} <button onClick={() => handleRemoveSkill(skill)}>×</button>
              </span>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label>Interests *</label>
          <div className="tag-input">
            <input
              type="text"
              value={interestInput}
              onChange={(e) => setInterestInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddInterest())}
              placeholder="e.g., Technology, Art, Business"
            />
            <button type="button" onClick={handleAddInterest}>Add</button>
          </div>
          <div className="tags">
            {formData.interests.map(interest => (
              <span key={interest} className="tag">
                {interest} <button onClick={() => handleRemoveInterest(interest)}>×</button>
              </span>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label>Location (City/State) *</label>
          <input
            type="text"
            value={formData.location}
            onChange={(e) => setFormData({...formData, location: e.target.value})}
            placeholder="e.g., Bangalore, Mumbai, Delhi"
            required
          />
        </div>

        <button type="submit" className="submit-btn">Get Recommendations</button>
      </form>
    </div>
  );
}

export default CareerForm;
