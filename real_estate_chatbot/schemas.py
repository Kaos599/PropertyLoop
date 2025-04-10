"""
Pydantic schemas for structured data output from the agents.
"""
from typing import List
from pydantic import BaseModel, Field

class PropertyIssueReport(BaseModel):
    """
    Structured schema for property issue detection results from Agent 1.
    """
    issue_assessment: str = Field(
        description="Detailed description of identified problems in the image."
    )
    troubleshooting_suggestions: List[str] = Field(
        description="Actionable advice for addressing identified issues."
    )
    professional_referral: List[str] = Field(
        description="Recommendations for specific professionals (e.g., Plumber, Electrician)."
    )
    safety_warnings: List[str] = Field(
        description="Urgent safety warnings for potential hazards detected.",
        default=[]
    )
