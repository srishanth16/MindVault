
import sys
from pathlib import Path
import time
import threading

log_file = Path(__file__).parent / "step_by_step_import3.log"
f = open(log_file, "w", encoding="utf-8", buffering=1)

sys.stdout = f
sys.stderr = f

done = False


def watchdog():
    time.sleep(30)  # 30s timeout
    if not done:
        log("WATCHDOG: import is taking too long! Printing tracebacks of all threads")
        import traceback
        for thread_id, frame in sys._current_frames().items():
            log(f"Thread {thread_id}:")
            log("".join(traceback.format_stack(frame)))
        log("WATCHDOG: exiting with code 1")
        os._exit(1)


threading.Thread(target=watchdog, daemon=True).start()


def log(msg):
    t = time.strftime("%H:%M:%S")
    print(f"[{t}] {msg}")
    f.flush()


log("Starting step by step import 3")

log("Step 1: import app.api.notes")
try:
    import app.api.notes
    log("✓ app.api.notes imported")
except Exception as e:
    log(f"✗ app.api.notes failed: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("Step 2: import app.api.chat")
try:
    import app.api.chat
    log("✓ app.api.chat imported")
except Exception as e:
    log(f"✗ app.api.chat failed: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("Step 3: import app.api.search")
try:
    import app.api.search
    log("✓ app.api.search imported")
except Exception as e:
    log(f"✗ app.api.search failed: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

done = True
log("All steps done!")
