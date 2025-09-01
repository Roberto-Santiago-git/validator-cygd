import sys, subprocess
BASE = [sys.executable, "-m", "cygd_validator.cli",
        "--engine", "powershell", "--policy", "policies/powershell.json"]
failed = []
for f in sys.argv[1:]:
    r = subprocess.run(BASE + [f])
    if r.returncode != 0:
        failed.append(f)
if failed:
    print("Archivos con error:")
    for f in failed:
        print(" -", f)
    sys.exit(1)
