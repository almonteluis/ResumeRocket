from typing import Dict, List
import json
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64
import seaborn as sns
import pandas as pd

class ResumeReportGenerator:
    def __init__(self):
        self.report_types = {
            "simple": self._generate_simple_report,
            "detailed": self._generate_detailed_report,
            "comparison": self._generate_comparison_report
        }

    def generate_report(self, analysis_data: Dict, report_type: str = "detailed") -> Dict:
        """Generate a report based on analysis data."""
        if report_type not in self.report_types:
            raise ValueError(f"Unknown report type: {report_type}")
            
        return self.report_types[report_type](analysis_data)

    def _generate_charts(self, analysis_data: Dict) -> Dict[str, str]:
        """Generate visualization charts."""
        charts = {}
        
        # Skills Match Chart
        plt.figure(figsize=(10, 6))
        skills_data = {
            'Matching': len(analysis_data['skills_match']['matching_skills']),
            'Missing': len(analysis_data['skills_match']['missing_skills']),
            'Extra': len(analysis_data['skills_match']['extra_skills'])
        }
        plt.pie(skills_data.values(), labels=skills_data.keys(), autopct='%1.1f%%')
        plt.title('Skills Distribution')
        charts['skills_chart'] = self._fig_to_base64()

        # Match Score Timeline
        if 'historical_scores' in analysis_data:
            plt.figure(figsize=(10, 6))
            dates = [score['date'] for score in analysis_data['historical_scores']]
            scores = [score['value'] for score in analysis_data['historical_scores']]
            plt.plot(dates, scores, marker='o')
            plt.title('Match Score Timeline')
            plt.xticks(rotation=45)
            plt.ylabel('Match Score (%)')
            charts['timeline_chart'] = self._fig_to_base64()

        # Experience Relevance Heatmap
        if 'experience_relevance' in analysis_data:
            plt.figure(figsize=(8, 6))
            relevance_data = {
                'Overall Relevance': analysis_data['experience_relevance']['overall_relevance'],
                'Recent Experience': 90 if analysis_data['experience_relevance']['has_recent_relevant_experience'] else 30
            }
            sns.heatmap(
                pd.DataFrame([relevance_data]).T,
                annot=True,
                cmap='RdYlGn',
                fmt='.0f'
            )
            plt.title('Experience Relevance Analysis')
            charts['relevance_chart'] = self._fig_to_base64()

        return charts

    def _fig_to_base64(self) -> str:
        """Convert matplotlib figure to base64 string."""
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode('utf-8')

    def _generate_detailed_report(self, analysis_data: Dict) -> Dict:
        """Generate a detailed report with visualizations."""
        charts = self._generate_charts(analysis_data)
        
        return {
            "report_type": "detailed",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "overall_match_score": analysis_data["match_score"],
                "experience_level": analysis_data["experience_level"],
                "skills_match_percentage": analysis_data["skills_match"]["match_percentage"]
            },
            "skills_analysis": {
                "matching_skills": analysis_data["skills_match"]["matching_skills"],
                "missing_skills": analysis_data["skills_match"]["missing_skills"],
                "extra_skills": analysis_data["skills_match"]["extra_skills"]
            },
            "experience_analysis": {
                "relevance_score": analysis_data["experience_relevance"]["overall_relevance"],
                "relevant_experience_count": analysis_data["experience_relevance"]["relevant_experience_count"]
            },
            "suggestions": analysis_data["improvement_suggestions"],
            "visualizations": charts
        }

    def _generate_simple_report(self, analysis_data: Dict) -> Dict:
        """Generate a simple summary report."""
        return {
            "report_type": "simple",
            "generated_at": datetime.now().isoformat(),
            "match_score": analysis_data["match_score"],
            "key_missing_skills": analysis_data["skills_match"]["missing_skills"][:5],
            "key_suggestions": analysis_data["improvement_suggestions"][:3]
        }

    def _generate_comparison_report(self, analysis_data: Dict) -> Dict:
        """Generate a comparison report against similar job descriptions."""
        # Implement comparison logic here
        pass