
import sys
from pathlib import Path
import time

log_file = Path(__file__).parent / "test_import_note.log"
f = open(log_file, "w", encoding="utf-8", buffering=1)

sys.stdout = f
sys.stderr = f


def log(msg):
    t = time.strftime("%H:%M:%S")
    print(f"[{t}] {msg}")
    f.flush()


log("Testing import app.models.note")
try:
    log("1. Importing pydantic...")
    import pydantic
    log("   ok")
except Exception as e:
    log(f"   fail: {e}")

try:
    log("2. Importing app.models.note...")
    import app.models.note
    log("   ok")
    log("   NoteCreate: " + str(app.models.note.NoteCreate))
except Exception as e:
    log(f"   fail: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)
