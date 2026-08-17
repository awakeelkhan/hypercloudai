from pathlib import Path

def search_project(query):
    results = []
    for path in Path(".").rglob("*"):
        if path.is_file() and ".git" not in path.parts and "virtualenv" not in path.parts:
            try:
                text = path.read_text(errors="ignore")
                if query.lower() in text.lower():
                    results.append(str(path))
            except Exception:
                pass
    return results