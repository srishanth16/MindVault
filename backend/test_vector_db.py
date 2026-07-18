
import sys
from pathlib import Path

log_file = Path(__file__).parent / "test_vector_db.log"
log_file.write_text("")

def log(msg):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

try:
    log("Attempting to import app.services.vector_db...")
    import app.services.vector_db
    log("✓ Success!")
    log("Calling get_vector_store...")
    store = app.services.vector_db.get_vector_store()
    log("✓ get_vector_store returned!")
    log(f"Store: {store}")
except Exception as e:
    log(f"✗ Failed: {type(e).__name__}: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)
