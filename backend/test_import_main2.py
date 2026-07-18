
import sys
from pathlib import Path

log_file = Path(__file__).parent / "test_import_main2.log"
f = open(log_file, "w", encoding="utf-8", buffering=1)

sys.stdout = f
sys.stderr = f

print("test_import_main2.py starting")
print("1. Trying to import app.main...")
try:
    import app.main
    print("   OK!")
except Exception as e:
    print(f"Failed to import app.main: {type(e)} {e}")
    import traceback
    print(traceback.format_exc())
    sys.exit(1)

print("2. Trying to get app...")
try:
    from app.main import app
    print("   OK!")
    print(f"app: {app}")
except Exception as e:
    print(f"Failed to get app: {type(e)} {e}")
    import traceback
    print(traceback.format_exc())
    sys.exit(1)
