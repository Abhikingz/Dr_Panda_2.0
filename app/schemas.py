from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    user_message: str
    patient_age: Optional[int] = 30

class MatchResult(BaseModel):
    condition: str
    urgency_level: str
    action_recommendation: str
    home_care_advice: str
    confidence_score: float

class ChatResponse(BaseModel):
    panda_reply: str
    match_result: MatchResult
    disclaimer: str

class ReportAnalysisResponse(BaseModel):
    extracted_text: str
    detected_markers: List[dict]
    overall_health_insight: str
    hospital_visit_required: bool
    urgency_rating: str
    disclaimer: str
