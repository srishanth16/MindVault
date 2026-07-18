
import sys
from pathlib import Path
import time

log_file = Path(__file__).parent / "step_by_step_import.log"
f = open(log_file, "w", encoding="utf-8", buffering=1)

sys.stdout = f
sys.stderr = f


def log(msg):
    t = time.strftime("%H:%M:%S")
    print(f"[{t}] {msg}")
    f.flush()


log("Starting step by step import")

log("Step 1: import app.config")
try:
    import app.config
    log("✓ app.config imported")
except Exception as e:
    log(f"✗ app.config failed: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("Step 2: import app.database")
try:
    import app.database
    log("✓ app.database imported")
except Exception as e:
    log(f"✗ app.database failed: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("Step 3: import app.middleware.auth_middleware")
try:
    import app.middleware.auth_middleware
    log("✓ app.middleware.auth_middleware imported")
except Exception as e:
    log(f"✗ app.middleware.auth_middleware failed: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("Step 4: import app.api.auth")
try:
    import app.api.auth
    log("✓ app.api.auth imported")
except Exception as e:
    log(f"✗ app.api.auth failed: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("Step 5: import app.api.documents")
try:
    import app.api.documents
    log("✓ app.api.documents imported")
except Exception as e:
    log(f"✗ app.api.documents failed: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("Step 6: import app.api.folders")
try:
    import app.api.folders
    log("✓ app.api.folders imported")
except Exception as e:
    log(f"✗ app.api.folders failed: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("Step 7: import app.api.notes")
try:
    import app.api.notes
    log("✓ app.api.notes imported")
except Exception as e:
    log(f"✗ app.api.notes failed: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("Step 8: import app.api.stats")
try:
    import app.api.stats
    log("✓ app.api.stats imported")
except Exception as e:
    log(f"✗ app.api.stats failed: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("Step 9: import app.api.chat")
try:
    import app.api.chat
    log("✓ app.api.chat imported")
except Exception as e:
    log(f"✗ app.api.chat failed: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("Step 10: import app.api.search")
try:
    import app.api.search
    log("✓ app.api.search imported")
except Exception as e:
    log(f"✗ app.api.search failed: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("Step 11: import app.main")
try:
    import app.main
    log("✓ app.main imported")
except Exception as e:
    log(f"✗ app.main failed: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("All steps done!")
