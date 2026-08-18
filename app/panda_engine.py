import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class PandaDoctorEngine:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, "data", "medical_qa_dataset.csv")
        self.df = pd.read_csv(csv_path)
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["symptom_query"])

    def process_query(self, user_query: str):
        query_vec = self.vectorizer.transform([user_query.lower()])
        scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        top_idx = int(np.argmax(scores))
        max_score = float(scores[top_idx])
        
        row = self.df.iloc[top_idx]
        conf = max(0.65, min(0.97, max_score + 0.55)) if max_score > 0 else 0.50
        
        # Panda doctor personality responses
        panda_greetings = [
            "Hello there, I am Dr. Panda. I am carefully reviewing your symptoms.",
            "Dr. Panda here. Let us check your symptoms step by step.",
            "Greetings, I am Dr. Panda. I have analyzed your health query."
        ]
        greeting = panda_greetings[len(user_query) % len(panda_greetings)]
        
        reply = f"{greeting} Based on what you described, this shows similarity to {row['condition']}. My assessment rating is {row['urgency']} priority."
        
        return {
            "panda_reply": reply,
            "condition": row["condition"],
            "urgency_level": row["urgency"],
            "action_recommendation": row["action"],
            "home_care_advice": row["home_care"],
            "confidence_score": round(conf, 4)
        }
