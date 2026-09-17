from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = REPO_ROOT / "data"
RAW_DIR = DATA_ROOT / "raw"
PROCESSED_DIR = DATA_ROOT / "processed"
ARTIFACT_DIR = REPO_ROOT / "artifacts"
EVIDENCE_DIR = REPO_ROOT / "evidence"

