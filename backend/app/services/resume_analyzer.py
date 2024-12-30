from typing import Dict, List, Optional
import spacy
from collections import Counter
from datetime import datetime
import re

class ResumeAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        
        # Define common job titles and their variations
        self.job_titles = {
            "software_engineer": [
                "software engineer", "software developer", "programmer",
                "full stack", "backend", "frontend", "DevOps"
            ],
            "data_scientist": [
                "data scientist", "machine learning", "AI engineer",
                "ML engineer", "data analyst"
            ],
            # Add more job categories as needed
        }
        
        # Define experience levels
        self.experience_levels = {
            "entry": ["intern", "junior", "entry level", "associate"],
            "mid": ["mid level", "intermediate", "regular"],
            "senior": ["senior", "lead", "principal", "architect", "manager"]
        }

    def analyze_resume_for_job(self, resume_text: str, job_description: str) -> Dict:
        """Comprehensive resume analysis for a specific job."""
        try:
            resume_doc = self.nlp(resume_text)
            job_doc = self.nlp(job_description)
            
            # Basic similarity score
            similarity_score = resume_doc.similarity(job_doc)
            
            # Analyze experience level
            experience_level = self._determine_experience_level(resume_text)
            
            # Extract and match skills
            skills_analysis = self._analyze_skills(resume_text, job_description)
            
            # Analyze work experience relevance
            experience_analysis = self._analyze_experience_relevance(
                resume_text, job_description
            )
            
            # Generate improvement suggestions
            suggestions = self._generate_suggestions(
                skills_analysis,
                experience_analysis,
                similarity_score
            )
            
            return {
                "match_score": round(similarity_score * 100, 2),
                "experience_level": experience_level,
                "skills_match": skills_analysis,
                "experience_relevance": experience_analysis,
                "improvement_suggestions": suggestions,
                "analysis_timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            raise Exception(f"Error analyzing resume: {str(e)}")

    def _determine_experience_level(self, text: str) -> str:
        """Determine the experience level based on resume content."""
        text_lower = text.lower()
        
        # Count years of experience mentions
        years_pattern = r'(\d+)[\+\s]*(?:years?|yrs?)(?:\s+of)?\s+experience'
        years_matches = re.findall(years_pattern, text_lower)
        max_years = max([int(y) for y in years_matches]) if years_matches else 0
        
        # Check title mentions
        level_counts = {
            level: sum(1 for term in terms if term in text_lower)
            for level, terms in self.experience_levels.items()
        }
        
        # Determine level based on years and title mentions
        if max_years > 8 or level_counts['senior'] > 0:
            return "senior"
        elif max_years > 3 or level_counts['mid'] > 0:
            return "mid"
        else:
            return "entry"

    def _analyze_skills(self, resume_text: str, job_description: str) -> Dict:
        """Analyze skills match between resume and job description."""
        # Extract skills from both texts
        resume_skills = self._extract_skills(resume_text)
        job_skills = self._extract_skills(job_description)
        
        # Calculate matches and gaps
        matching_skills = set(resume_skills) & set(job_skills)
        missing_skills = set(job_skills) - set(resume_skills)
        extra_skills = set(resume_skills) - set(job_skills)
        
        # Calculate skill match percentage
        match_percentage = len(matching_skills) / len(job_skills) * 100 if job_skills else 0
        
        return {
            "matching_skills": list(matching_skills),
            "missing_skills": list(missing_skills),
            "extra_skills": list(extra_skills),
            "match_percentage": round(match_percentage, 2)
        }

    def _analyze_experience_relevance(self, resume_text: str, job_description: str) -> Dict:
        """Analyze how relevant the work experience is to the job."""
        resume_doc = self.nlp(resume_text)
        job_doc = self.nlp(job_description)
        
        # Extract work experience sections
        experience_pattern = r'(?:EXPERIENCE|WORK EXPERIENCE|EMPLOYMENT).*?(?=\n\n[A-Z]|$)'
        experience_matches = re.findall(experience_pattern, resume_text, re.DOTALL | re.I)
        
        relevance_scores = []
        if experience_matches:
            for exp in experience_matches:
                exp_doc = self.nlp(exp)
                relevance_scores.append(exp_doc.similarity(job_doc))
        
        avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0
        
        return {
            "overall_relevance": round(avg_relevance * 100, 2),
            "relevant_experience_count": len(relevance_scores),
            "has_recent_relevant_experience": avg_relevance > 0.6
        }

    def _generate_suggestions(
        self,
        skills_analysis: Dict,
        experience_analysis: Dict,
        similarity_score: float
    ) -> List[str]:
        """Generate improvement suggestions based on analysis."""
        suggestions = []
        
        # Skills-based suggestions
        if skills_analysis["missing_skills"]:
            suggestions.append(
                f"Consider adding these key skills: {', '.join(skills_analysis['missing_skills'][:5])}"
            )
        
        # Experience-based suggestions
        if experience_analysis["overall_relevance"] < 60:
            suggestions.append(
                "Highlight more relevant work experiences that align with the job requirements"
            )
        
        # Overall match suggestions
        if similarity_score < 0.6:
            suggestions.append(
                "Your resume might need significant adjustments to better match this role"
            )
        
        return suggestions

    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical and professional skills from text."""
        doc = self.nlp(text)
        
        # Extract potential skills (nouns and proper nouns)
        potential_skills = [
            token.text.lower() for token in doc 
            if (token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2)
        ]
        
        # Count skill occurrences
        skill_counts = Counter(potential_skills)
        
        # Filter common words and return significant skills
        common_words = set(['experience', 'year', 'work', 'team', 'project'])
        skills = [
            skill for skill, count in skill_counts.items()
            if skill not in common_words and count >= 1
        ]
        
        return skills