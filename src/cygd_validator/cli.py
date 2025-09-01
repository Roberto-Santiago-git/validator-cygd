import argparse, sys
from .core import validate

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", choices=["oracle","powershell","ipc"], required=False)
    ap.add_argument("--policy", required=True)
    ap.add_argument("path", nargs="?")
    args = ap.parse_args()
    data = sys.stdin.read() if not args.path else open(args.path,"r",encoding="utf-8",errors="ignore").read()
    fn = args.path or "stdin.txt"
    print(validate(data, fn, args.engine, args.policy))

if __name__=="__main__":
    main()
