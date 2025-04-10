"""
Pydantic schemas for structured data output from the agents.
"""
from typing import List, Optional
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

class TenancyFAQResponse(BaseModel):
    """
    Structured schema for tenancy FAQ responses from Agent 2.
    """
    answer: str = Field(
        description="Main answer to the user's tenancy-related question."
    )
    legal_references: List[str] = Field(
        description="Relevant laws, regulations, or legal principles referenced.",
        default=[]
    )
    regional_specifics: Optional[str] = Field(
        description="Location-specific information if a location was provided.",
        default=None
    )
    disclaimer: str = Field(
        description="Legal disclaimer indicating this is not legal advice.",
        default="This information is provided as general guidance and should not be considered legal advice. Laws and regulations vary by location and may change over time. Consult a legal professional for specific advice."
    )
    additional_resources: List[str] = Field(
        description="Additional resources or organizations the user can contact for more help.",
        default=[]
    )
