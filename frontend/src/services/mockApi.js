/**
 * Mock API for local development without AWS
 */

// Import the Python logic (we'll simulate it in JS)
const intentPatterns = {
  exploration: [
    /\b(explore|discover|learn about|what are|tell me about)\b.*\bcareer/i,
    /\bcareer\s+(options|paths|choices)/i,
    /\bjust\s+(looking|browsing)/i,
  ],
  personalized_guidance: [
    /\b(recommend|suggest|help me choose|guide me)\b/i,
    /\bwhat\s+career\s+(should|can)\s+i/i,
    /\bbest\s+career\s+for\s+me/i,
    /\bmy\s+(skills|interests|background)/i,
  ],
};

const careersData = [
  {
    title: 'Software Engineer',
    category: 'Technology',
    required_skills: ['python', 'java', 'problem_solving', 'algorithms', 'coding'],
    education_paths: ['btech', 'bsc', 'mtech'],
    related_interests: ['technology', 'problem_solving', 'innovation', 'computers'],
    demand_by_region: {
      bangalore: 0.95,
      hyderabad: 0.90,
      pune: 0.85,
      delhi_ncr: 0.88,
      mumbai: 0.82,
      national_avg: 0.75
    },
    salary_range: '₹4-15 LPA',
    growth_outlook: 'Excellent',
    min_education: 'B.Tech/B.Sc'
  },
  {
    title: 'Data Scientist',
    category: 'Technology',
    required_skills: ['python', 'statistics', 'machine_learning', 'sql', 'data_analysis'],
    education_paths: ['btech', 'mtech', 'msc'],
    related_interests: ['data_analysis', 'mathematics', 'research', 'technology'],
    demand_by_region: {
      bangalore: 0.92,
      mumbai: 0.88,
      delhi_ncr: 0.85,
      pune: 0.83,
      national_avg: 0.70
    },
    salary_range: '₹6-20 LPA',
    growth_outlook: 'Excellent',
    min_education: 'B.Tech/M.Sc'
  },
  {
    title: 'Digital Marketing Specialist',
    category: 'Marketing',
    required_skills: ['seo', 'content_writing', 'social_media', 'analytics', 'communication'],
    education_paths: ['12th_commerce', '12th_arts', 'bcom', 'ba', 'mba'],
    related_interests: ['creativity', 'communication', 'business', 'social_media'],
    demand_by_region: {
      mumbai: 0.90,
      delhi_ncr: 0.88,
      bangalore: 0.85,
      pune: 0.82,
      national_avg: 0.75
    },
    salary_range: '₹3-10 LPA',
    growth_outlook: 'Very Good',
    min_education: '12th/Graduation'
  },
  {
    title: 'Chartered Accountant',
    category: 'Finance',
    required_skills: ['accounting', 'taxation', 'auditing', 'financial_analysis'],
    education_paths: ['12th_commerce', 'bcom'],
    related_interests: ['finance', 'mathematics', 'business', 'analysis'],
    demand_by_region: {
      mumbai: 0.92,
      delhi_ncr: 0.88,
      bangalore: 0.85,
      pune: 0.82,
      national_avg: 0.78
    },
    salary_range: '₹6-25 LPA',
    growth_outlook: 'Excellent',
    min_education: '12th Commerce'
  },
  {
    title: 'Graphic Designer',
    category: 'Design',
    required_skills: ['photoshop', 'illustrator', 'creativity', 'design', 'visual_communication'],
    education_paths: ['12th_arts', 'diploma', 'ba'],
    related_interests: ['art', 'creativity', 'design', 'visual_arts'],
    demand_by_region: {
      mumbai: 0.85,
      bangalore: 0.82,
      delhi_ncr: 0.80,
      pune: 0.75,
      national_avg: 0.68
    },
    salary_range: '₹2.5-8 LPA',
    growth_outlook: 'Good',
    min_education: '12th/Diploma'
  },
  {
    title: 'Content Writer',
    category: 'Media',
    required_skills: ['writing', 'communication', 'creativity', 'research', 'seo'],
    education_paths: ['12th_arts', 'ba', 'bcom'],
    related_interests: ['writing', 'creativity', 'communication', 'storytelling'],
    demand_by_region: {
      bangalore: 0.82,
      mumbai: 0.80,
      delhi_ncr: 0.78,
      pune: 0.75,
      national_avg: 0.70
    },
    salary_range: '₹2-6 LPA',
    growth_outlook: 'Good',
    min_education: '12th/Graduation'
  },
]
    