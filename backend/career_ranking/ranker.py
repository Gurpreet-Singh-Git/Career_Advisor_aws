"""
Career Ranking Engine
ML-based scoring system with explainable weighted ranking
"""
import json
from typing import List, Dict

try:
    import boto3
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

class CareerRanker:
    """Ranks careers based on user profile using explainable scoring"""
    
    def __init__(self):
        if HAS_BOTO3:
            self.s3_client = boto3.client('s3')
            self.bucket_name = 'career-guidance-data'
        else:
            self.s3_client = None
        self.careers_data = self._load_careers_data()
        
        # Scoring weights (explainable and tunable)
        self.weights = {
            'skill_match': 0.35,
            'education_fit': 0.25,
            'interest_alignment': 0.25,
            'regional_demand': 0.15
        }
    
    def _load_careers_data(self):
        """Load career dataset from S3 or local file"""
        # Try local file first (multiple possible paths)
        for path in ['data/careers.json', '../data/careers.json', './data/careers.json']:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✓ Loaded {len(data)} careers from {path}")
                    return data
            except:
                continue
        
        # Try S3 if boto3 available
        if HAS_BOTO3 and self.s3_client:
            try:
                response = self.s3_client.get_object(
                    Bucket=self.bucket_name,
                    Key='careers.json'
                )
                return json.loads(response['Body'].read())
            except Exception as e:
                pass
        
        # Fallback to sample data
        print("⚠ Using sample data (careers.json not found)")
        return self._get_sample_careers()
    
    def rank(self, education: str, skills: List[str], 
             interests: List[str], location: str) -> List[Dict]:
        """
        Rank careers based on user profile
        
        Args:
            education: Education level (e.g., '12th_science', 'btech_cs')
            skills: List of skills
            interests: List of interests
            location: City/state in India
            
        Returns:
            List of top 3 ranked careers with score breakdown
        """
        scored_careers = []
        
        for career in self.careers_data:
            # Calculate individual scores
            skill_score = self._calculate_skill_match(skills, career['required_skills'])
            education_score = self._calculate_education_fit(education, career['education_paths'])
            interest_score = self._calculate_interest_alignment(interests, career['related_interests'])
            regional_score = self._calculate_regional_demand(location, career['demand_by_region'])
            
            # Calculate weighted total score
            total_score = (
                self.weights['skill_match'] * skill_score +
                self.weights['education_fit'] * education_score +
                self.weights['interest_alignment'] * interest_score +
                self.weights['regional_demand'] * regional_score
            )
            
            scored_careers.append({
                'title': career['title'],
                'category': career['category'],
                'score': round(total_score, 2),
                'breakdown': {
                    'skill_match': round(skill_score, 2),
                    'education_fit': round(education_score, 2),
                    'interest_alignment': round(interest_score, 2),
                    'regional_demand': round(regional_score, 2)
                },
                'metadata': {
                    'avg_salary_range': career.get('salary_range', 'Varies'),
                    'growth_outlook': career.get('growth_outlook', 'Moderate'),
                    'education_required': career.get('min_education', 'Varies')
                }
            })
        
        # Sort by score and return top 3
        scored_careers.sort(key=lambda x: x['score'], reverse=True)
        return scored_careers[:3]
    
    def _calculate_skill_match(self, user_skills: List[str], required_skills: List[str]) -> float:
        """Calculate skill match score using Jaccard similarity"""
        if not required_skills:
            return 0.5  # Neutral score if no skills specified
        
        user_skills_lower = [s.lower() for s in user_skills]
        required_skills_lower = [s.lower() for s in required_skills]
        
        intersection = len(set(user_skills_lower) & set(required_skills_lower))
        union = len(set(user_skills_lower) | set(required_skills_lower))
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_education_fit(self, user_education: str, education_paths: List[str]) -> float:
        """Calculate education compatibility score"""
        education_hierarchy = {
            '10th': 1,
            '12th_science': 2,
            '12th_commerce': 2,
            '12th_arts': 2,
            'diploma': 3,
            'btech': 4,
            'bsc': 4,
            'bcom': 4,
            'ba': 4,
            'mtech': 5,
            'msc': 5,
            'mba': 5,
            'phd': 6
        }
        
        user_level = education_hierarchy.get(user_education.lower(), 0)
        
        # Check if user meets minimum requirement
        for path in education_paths:
            required_level = education_hierarchy.get(path.lower(), 0)
            if user_level >= required_level:
                return 1.0
        
        # Partial score if close
        min_required = min([education_hierarchy.get(p.lower(), 0) for p in education_paths])
        gap = min_required - user_level
        
        if gap == 1:
            return 0.7
        elif gap == 2:
            return 0.4
        else:
            return 0.1
    
    def _calculate_interest_alignment(self, user_interests: List[str], 
                                     career_interests: List[str]) -> float:
        """Calculate interest alignment score"""
        if not career_interests:
            return 0.5
        
        user_interests_lower = [i.lower() for i in user_interests]
        career_interests_lower = [i.lower() for i in career_interests]
        
        matches = len(set(user_interests_lower) & set(career_interests_lower))
        return min(matches / len(career_interests_lower), 1.0)
    
    def _calculate_regional_demand(self, location: str, demand_by_region: Dict) -> float:
        """Calculate regional demand score"""
        location_lower = location.lower()
        
        # Check for exact match
        if location_lower in demand_by_region:
            return demand_by_region[location_lower]
        
        # Check for state/region match
        region_mapping = {
            'bangalore': 'karnataka',
            'mumbai': 'maharashtra',
            'delhi': 'delhi_ncr',
            'hyderabad': 'telangana',
            'chennai': 'tamil_nadu',
            'pune': 'maharashtra',
            'kolkata': 'west_bengal'
        }
        
        region = region_mapping.get(location_lower)
        if region and region in demand_by_region:
            return demand_by_region[region]
        
        # Default to national average
        return demand_by_region.get('national_avg', 0.5)
    
    def _get_sample_careers(self):
        """Sample career data for development"""
        return [
            {
                'title': 'Software Engineer',
                'category': 'Technology',
                'required_skills': ['python', 'java', 'problem_solving', 'algorithms'],
                'education_paths': ['btech', 'bsc', 'mtech'],
                'related_interests': ['technology', 'problem_solving', 'innovation'],
                'demand_by_region': {
                    'bangalore': 0.95,
                    'hyderabad': 0.90,
                    'pune': 0.85,
                    'delhi_ncr': 0.88,
                    'national_avg': 0.75
                },
                'salary_range': '₹4-15 LPA',
                'growth_outlook': 'Excellent',
                'min_education': 'B.Tech/B.Sc'
            },
            {
                'title': 'Data Scientist',
                'category': 'Technology',
                'required_skills': ['python', 'statistics', 'machine_learning', 'sql'],
                'education_paths': ['btech', 'mtech', 'msc'],
                'related_interests': ['data_analysis', 'mathematics', 'research'],
                'demand_by_region': {
                    'bangalore': 0.92,
                    'mumbai': 0.88,
                    'delhi_ncr': 0.85,
                    'national_avg': 0.70
                },
                'salary_range': '₹6-20 LPA',
                'growth_outlook': 'Excellent',
                'min_education': 'B.Tech/M.Sc'
            },
            {
                'title': 'Digital Marketing Specialist',
                'category': 'Marketing',
                'required_skills': ['seo', 'content_writing', 'social_media', 'analytics'],
                'education_paths': ['12th_commerce', 'bcom', 'ba', 'mba'],
                'related_interests': ['creativity', 'communication', 'business'],
                'demand_by_region': {
                    'mumbai': 0.90,
                    'delhi_ncr': 0.88,
                    'bangalore': 0.85,
                    'national_avg': 0.75
                },
                'salary_range': '₹3-10 LPA',
                'growth_outlook': 'Very Good',
                'min_education': '12th/Graduation'
            }
        ]
