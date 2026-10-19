
from pathlib import Path


def test_source_files_exist():
    root = Path(__file__).resolve().parents[2]

    assert (root / "backend" / "app.py").exists()
    assert (root / "airline-frontend" / "package.json").exists()
    assert (root / "README.md").exists()
    assert (root / "requirements.txt").exists()
