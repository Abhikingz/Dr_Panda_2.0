import os
import pandas as pd

class MedicalReportAnalyzer:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.benchmarks = pd.read_csv(os.path.join(base_dir, "data", "lab_test_benchmarks.csv"))

    def analyze_report_text(self, text_content: str):
        text_lower = text_content.lower()
        detected = []
        hospital_needed = False
        urgency = "Low"
        
        for idx, row in self.benchmarks.iterrows():
            marker = row["test_name"].lower()
            if any(term in text_lower for term in marker.split()):
                detected.append({
                    "test_name": row["test_name"],
                    "normal_range": row["normal_range"],
                    "insight": row["insight"]
                })
                
        if "high" in text_lower or "elevated" in text_lower or "positive" in text_lower or "abnormal" in text_lower:
            urgency = "Moderate"
            if "severe" in text_lower or "critical" in text_lower or "emergency" in text_lower:
                hospital_needed = True
                urgency = "Emergency"
                
        summary_insight = f"Dr. Panda analyzed your report and identified {len(detected)} health markers. Overall risk priority is rated as {urgency}."
        if hospital_needed:
            summary_insight += " Immediate hospital evaluation is advised based on critical flags in the uploaded report."
        elif urgency == "Moderate":
            summary_insight += " Schedule a medical consultation to review these lab figures with a practitioner."
        else:
            summary_insight += " Results appear within manageable limits. Continue regular wellness checkups and healthy hydration."

        return {
            "extracted_text_preview": text_content[:300] + "..." if len(text_content) > 300 else text_content,
            "detected_markers": detected,
            "overall_health_insight": summary_insight,
            "hospital_visit_required": hospital_needed,
            "urgency_rating": urgency
        }
