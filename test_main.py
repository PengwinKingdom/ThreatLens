from main import analyze_file


def test_file_analysis():
    result = analyze_file("sample.txt")

    assert result is not None
    assert result["file_name"] == "sample.txt"
    assert result["file_size"] > 0
    assert len(result["sha256"]) == 64
    assert isinstance(result["yara_matches"], list)



def test_yara_positive(tmp_path):
    test_file = tmp_path / "positive.txt"
    test_file.write_text("THREATLENS_TEST_SIGNATURE")

    result = analyze_file(test_file)

    assert "ThreatLens_Test" in result["yara_matches"]



def test_yara_negative(tmp_path):
    test_file = tmp_path / "negative.txt"
    test_file.write_text("This is a harmless test file.")

    result = analyze_file(test_file)

    assert result["yara_matches"] == []


def test_missing_file(tmp_path):
    missing_file = tmp_path / "missing.txt"

    result = analyze_file(missing_file)

    assert "error" in result
    assert "File not found" in result["error"]