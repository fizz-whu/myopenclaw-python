from typing import Dict, Optional, List
from datetime import datetime
import json
from pathlib import Path


class Message:
    def __init__(self, role: str, content: str, timestamp: Optional[float] = None):
        self.role = role
        self.content = content
        self.timestamp = timestamp or datetime.now().timestamp()


class SessionEntry:
    def __init__(self, session_key: str):
        self.session_key = session_key
        self.messages: List[Message] = []
        self.created_at = datetime.now().timestamp()
        self.updated_at = datetime.now().timestamp()

    def add_message(self, role: str, content: str):
        self.messages.append(Message(role, content))
        self.updated_at = datetime.now().timestamp()


class SessionStore:
    def __init__(self, store_path: str = "sessions.json"):
        self.store_path = Path(store_path)
        self.sessions: Dict[str, SessionEntry] = {}
        self._load()

    def _load(self):
        if self.store_path.exists():
            try:
                with open(self.store_path, "r") as f:
                    data = json.load(f)
                    for key, entry_data in data.items():
                        entry = SessionEntry(key)
                        entry.created_at = entry_data.get("created_at", entry.created_at)
                        entry.updated_at = entry_data.get("updated_at", entry.updated_at)
                        entry.messages = [
                            Message(**msg) for msg in entry_data.get("messages", [])
                        ]
                        self.sessions[key] = entry
            except Exception:
                pass

    def _save(self):
        data = {}
        for key, entry in self.sessions.items():
            data[key] = {
                "created_at": entry.created_at,
                "updated_at": entry.updated_at,
                "messages": [
                    {"role": msg.role, "content": msg.content, "timestamp": msg.timestamp}
                    for msg in entry.messages
                ],
            }
        with open(self.store_path, "w") as f:
            json.dump(data, f, indent=2)

    def get_or_create(self, session_key: str) -> SessionEntry:
        if session_key not in self.sessions:
            self.sessions[session_key] = SessionEntry(session_key)
            self._save()
        return self.sessions[session_key]

    def update(self, session_key: str, entry: SessionEntry):
        self.sessions[session_key] = entry
        self._save()
