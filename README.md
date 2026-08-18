# Dr. Panda 2.0: AI Medical Intelligence Platform

Dr. Panda 2.0 is an expanded interactive healthcare platform incorporating symptom screening, an interactive panda doctor persona, medical report file parsing, and a triage urgency rating engine.

## Project Documentation & Technical Report

* **Download Technical PDF Report**: [Technical_Report_Dr_Panda_2.0.pdf](Technical_Report_Dr_Panda_2.0.pdf)
* **Primary Public Datasets**:
  * Medical QA Dataset in `data/medical_qa_dataset.csv`
  * Lab Test Benchmarks in `data/lab_test_benchmarks.csv`
  * Symptom Triage Rules in `data/symptom_triage_rules.csv`

## Key Capabilities

* Interactive Panda Doctor Persona providing supportive conversational triage guidance
* Automated Medical Report Reader parsing lab files for glucose, cholesterol, and blood cell markers
* Triage Rating Engine assigning care requirements across Emergency, Moderate, and Low priority tiers
* Prominent AI Exclamation Disclaimer highlighting suggestive screening limits

## Quickstart Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start FastAPI REST Backend
```bash
uvicorn app.main:app --reload --port 8000
```

### 3. Launch Dr. Panda 2.0 Web Interface
```bash
streamlit run app/frontend.py
```
