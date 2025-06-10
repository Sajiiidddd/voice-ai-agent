# app/metrics.py
import time
import pandas as pd
from datetime import datetime

class MetricsLogger:
    def __init__(self, filename="session_log.xlsx"):
        self.filename = filename
        self.rows = []

    def start_timer(self):
        return time.perf_counter()

    def log_turn(self, user_text, ai_text, t_eou, t_ttft, t_ttfb):
        latency_total = t_ttfb - t_eou
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.rows.append({
            "Timestamp": timestamp,
            "User Input": user_text,
            "AI Response": ai_text,
            "EOU Time": round(t_eou, 3),
            "TTFT": round(t_ttft - t_eou, 3),
            "TTFB": round(t_ttfb - t_ttft, 3),
            "Total Latency": round(latency_total, 3)
        })

    def save_to_excel(self):
        df = pd.DataFrame(self.rows)
        df.to_excel(self.filename, index=False)
        print(f"\n📊 Metrics saved to: {self.filename}")
