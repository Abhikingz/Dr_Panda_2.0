from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import time
from app.panda_engine import PandaDoctorEngine
from app.report_analyzer import MedicalReportAnalyzer

app = FastAPI(
    title="Dr. Panda 2.0 AI Medical Intelligence Service",
    description="Interactive Medical Screening, Symptom Analysis, and Lab Report Insights API",
    version="2.0.0"
)

panda_engine = PandaDoctorEngine()
report_analyzer = MedicalReportAnalyzer()

DISCLAIMER = "EXCLAMATION: Dr. Panda 2.0 is an AI medical assistant built for educational and suggestive screening purposes only. It is not responsible for medical outcomes and does not provide official medical diagnosis or treatment. Always consult a licensed healthcare professional for medical emergencies."

class QueryPayload(BaseModel):
    query: str

@app.get("/")
def root():
    return {"status": "online", "system": "Dr. Panda 2.0 AI Medical Assistant"}

@app.post("/api/v2/chat")
def chat_with_dr_panda(payload: QueryPayload):
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    res = panda_engine.process_query(payload.query)
    return {
        "response": res,
        "disclaimer": DISCLAIMER
    }

@app.post("/api/v2/analyze_report")
async def analyze_report(file: UploadFile = File(...)):
    contents = await file.read()
    text = contents.decode("utf-8", errors="ignore")
    analysis = report_analyzer.analyze_report_text(text)
    return {
        "analysis": analysis,
        "disclaimer": DISCLAIMER
    }
