def validate(text, policy):
    up = text.upper()
    findings=[]
    if policy.get("PS1-STRUCTURE", True) and "CLEAR-HOST" not in up:
        findings.append(dict(severity="MINOR", rule_id="PS1-STRUCTURE",
                             message="Incluye Clear-Host al inicio y cabecera estándar."))
    return findings
