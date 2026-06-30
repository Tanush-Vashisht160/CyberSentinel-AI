import json
from datetime import datetime
import os

LOG_FILE = "analyzer/logs.json"


def save_log(prompt, threats, score, severity):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prompt": prompt,
        "threats": threats,
        "score": score,
        "severity": severity
    }

    # Load existing logs
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    # Add new log
    data.append(log_entry)

    # Save back
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)