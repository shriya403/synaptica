import json
import os
from datetime import datetime

REPORTS_FILE = "storage/reports.json"


def load_reports():
    if not os.path.exists(REPORTS_FILE):
        return []

    try:
        with open(REPORTS_FILE, "r", encoding="utf-8") as f:
            data = f.read().strip()
            if not data:
                return []
            return json.loads(data)
    except Exception:
        return []


def save_report(title, content, source_type="rag"):
    reports = load_reports()

    report = {
        "id": len(reports) + 1,
        "title": title,
        "content": content,
        "source_type": source_type,
        "created_at": datetime.now().isoformat(),
    }

    reports.append(report)

    with open(REPORTS_FILE, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=4)

    return report


def clear_reports():
    with open(REPORTS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)

    return []