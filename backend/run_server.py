
import uvicorn
import sys
from pathlib import Path

# Redirect all output to server.log with unbuffered writing
log_file = Path(__file__).parent / "server.log"
f = open(log_file, "w", encoding="utf-8", buffering=1)  # line buffering
sys.stdout = f
sys.stderr = f

print("Starting server...")

if __name__ == "__main__":
    try:
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, log_level="debug")
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        print(traceback.format_exc())
        f.flush()
