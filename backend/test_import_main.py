
import sys
from pathlib import Path

log_file = Path(__file__).parent / "test_import_main.log"
f = open(log_file, "w", encoding="utf-8", buffering=1)

sys.stdout = f
sys.stderr = f

print("test_import_main.py starting")
print("1. Trying to import app.main...")
try:
    import app.main
    print("   OK!")
except Exception as e:
    print(f"Failed to import app.main: {type(e)}")
    import traceback
    print(traceback.format_exc())
    sys.exit(1)

print("2. Trying to get app...")
try:
    from app.main import app
    print("   OK!")
    print(f"app: {app}")
    print(f"app routes: {[route.path for route in app.routes}")
except Exception as e:
    print(f"Failed to get app: {type(e)}")
    import traceback
    print(traceback.format_exc())
    sys.exit(1)
