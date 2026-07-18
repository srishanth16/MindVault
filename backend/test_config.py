
import sys
from pathlib import Path

log_file = Path(__file__).parent / "test_config.log"
log_file.write_text("")

def log(msg):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

try:
    log("Attempting to import from app.config import settings...")
    from app.config import settings
    log("✓ Success!")
    log(f"MONGODB_URL: {settings.MONGODB_URL}")
    log(f"JWT_SECRET: {settings.JWT_SECRET}")
    log(f"UPLOAD_DIR: {settings.UPLOAD_DIR}")
except Exception as e:
    log(f"✗ Failed: {type(e).__name__}: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)
