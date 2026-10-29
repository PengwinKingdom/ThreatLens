from pathlib import Path
import hashlib
import yara


def analyze_file(file_path):
    path = Path(file_path)

    if not path.is_file():
        return {"error": "File not found or not a regular file."}

    try:
        file_size = path.stat().st_size
        file_hash = hashlib.sha256(path.read_bytes()).hexdigest()

        rules_path = (
            Path(__file__).resolve().parent
            / "rules"
            / "test_rule.yar"
        )

        rules = yara.compile(filepath=str(rules_path))
        matches = rules.match(filepath=str(path))

        return {
            "file_name": path.name,
            "file_size": file_size,
            "sha256": file_hash,
            "yara_matches": [match.rule for match in matches]
        }

    except OSError:
        return {"error": "Unable to read the file or rules."}

    except yara.Error:
        return {"error": "YARA analysis failed."}

if __name__ == "__main__":
    analysis = analyze_file("sample.txt")
    print(analysis)