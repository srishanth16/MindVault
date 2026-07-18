
import sys
from pathlib import Path
import time

log_file = Path(__file__).parent / "test_import_main3.log"
f = open(log_file, "w", encoding="utf-8", buffering=1)

sys.stdout = f
sys.stderr = f


def log(msg):
    t = time.strftime("%H:%M:%S")
    print(f"[{t}] {msg}")
    f.flush()


log("Testing import app.main and then running uvicorn")

log("1. Importing app.main")
try:
    import app.main
    log("✓ app.main imported")
except Exception as e:
    log(f"✗ app.main failed: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("2. Getting app")
try:
    from app.main import app
    log("✓ app got")
    log("  app routes:")
    for route in app.routes:
        log(f"    - {route.path}")
except Exception as e:
    log(f"✗ failed to get app: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("3. Now starting uvicorn")
try:
    import uvicorn
    log("  uvicorn imported")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
except Exception as e:
    log(f"✗ failed to run: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)
