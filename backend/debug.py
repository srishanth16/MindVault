
import sys
from pathlib import Path

# Write to a log file
log_file = Path(__file__).parent / "debug.log"
log_file.write_text("")

def log(msg):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

log("Starting debug script...")
log(f"Python version: {sys.version}")
log(f"CWD: {Path.cwd()}")
log(f"sys.path: {sys.path}")

try:
    log("1. Importing app.config...")
    import app.config
    log("✓ app.config imported!")
except Exception as e:
    log(f"✗ app.config failed: {type(e).__name__}: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

try:
    log("2. Importing app.database...")
    import app.database
    log("✓ app.database imported!")
except Exception as e:
    log(f"✗ app.database failed: {type(e).__name__}: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

try:
    log("3. Importing app.main...")
    import app.main
    log("✓ app.main imported!")
except Exception as e:
    log(f"✗ app.main failed: {type(e).__name__}: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("All imports succeeded! Now let's test app.main.app...")
try:
    from app.main import app
    log(f"✓ Got app: {app}")
except Exception as e:
    log(f"✗ Failed to get app: {type(e).__name__}: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("Done!")
