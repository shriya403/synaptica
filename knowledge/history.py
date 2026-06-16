import json
import os
from datetime import datetime

HISTORY_FILE = "storage/rag_history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = f.read().strip()
            if not data:
                return []
            return json.loads(data)
    except Exception:
        return []


def save_history_item(collection, question, answer, sources):
    history = load_history()

    history.append(
        {
            "timestamp": datetime.now().isoformat(),
            "collection": collection,
            "question": question,
            "answer": answer,
            "sources": sources,
        }
    )

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

    return history


def clear_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)

    return []