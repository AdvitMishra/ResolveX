import json
from pathlib import Path
from threading import RLock

class Store:
    def __init__(self, path):
        self.path, self.lock = Path(path), RLock()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists(): self.path.write_text("[]", encoding="utf-8")
    def _read(self):
        try: return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception: return []
    def all(self):
        with self.lock: return sorted(self._read(), key=lambda x:x.get("created_at",""), reverse=True)
    def get(self, iid):
        with self.lock: return next((x for x in self._read() if x["id"] == iid), None)
    def save(self, item):
        with self.lock:
            data=self._read()
            for i, old in enumerate(data):
                if old["id"] == item["id"]: data[i]=item; break
            else: data.append(item)
            self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return item
