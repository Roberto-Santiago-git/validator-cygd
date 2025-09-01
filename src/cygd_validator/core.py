import json, pathlib, re

def _detect_engine(filename, explicit):
    if explicit: return explicit
    ext = (pathlib.Path(filename).suffix or "").lower()
    if ext in (".sql",".ddl",".pkb",".pks",".pkg"): return "oracle"
    if ext in (".ps1",): return "powershell"
    if ext in (".xml",".txt"): return "oracle"  # por defecto
    return "oracle"

def format_report(findings):
    verdict = "CUMPLE" if not findings else "NO CUMPLE"
    parts = ["Validator CyGD", f"Validator Veredicto: {verdict}"]
    if findings:
        parts.append("")
        for f in findings:
            parts.append(f"[{f['severity']}] {f['rule_id']}: {f['message']}")
            parts.append("")
    return "\n".join(parts).rstrip()

def load_policy(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def run_rules(text, filename, engine, policy):
    if engine=="oracle":
        from .rules import oracle_sql as pack
    elif engine=="powershell":
        from .rules import powershell as pack
    elif engine=="ipc":
        from .rules import ipc as pack
    else:
        from .rules import oracle_sql as pack
    return pack.validate(text, policy)

def validate(text, filename, engine, policy_path):
    policy = load_policy(policy_path)
    eng = _detect_engine(filename, engine)
    findings = run_rules(text, filename, eng, policy)
    return format_report(findings)


