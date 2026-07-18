
from importlib.metadata import distributions
from pathlib import Path

log_file = Path(__file__).parent / "packages.log"
log_file.write_text("")

def log(msg):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

log("Checking installed packages:")
for dist in distributions():
    log(f"{dist.metadata['Name']}=={dist.version}")
