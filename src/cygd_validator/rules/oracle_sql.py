import re

VALID_PREFIXES = ("NB_","NU_","IM_","TP_","ST_","ID_","CD_","FH_","HR_","FL_")

# Detecta CREATE TABLE y captura el bloque de columnas entre paréntesis
CREATE_TBL_RE = re.compile(r"CREATE\s+TABLE\s+\S+\s*\((?P<body>[\s\S]*?)\)", re.I)

def _has_create_table(sql: str) -> bool:
    return bool(CREATE_TBL_RE.search(sql))

def _has_all_table_options(sql: str) -> bool:
    # Solo aplica a DDL de CREATE TABLE
    if not _has_create_table(sql):
        return True  # no marcar si no es objetivo de la regla
    return all(k in sql for k in ("TABLESPACE","COMPRESS","NOLOGGING","COMMENT ON TABLE"))

def _columns(sql: str):
    m = CREATE_TBL_RE.search(sql)
    if not m:
        return []
    raw = m.group("body")
    cols = []
    for line in raw.splitlines():
        line=line.strip().rstrip(",")
        if not line or line.upper().startswith(("CONSTRAINT","PRIMARY","FOREIGN")):
            continue
        name = re.split(r"\s+", line)[0].strip('"')
        cols.append(name)
    return cols

def validate(text, policy):
    findings=[]
    up = text.upper()

    if policy.get("ORA-TABLE-OPTIONS", True) and not _has_all_table_options(up):
        findings.append(dict(severity="MAJOR", rule_id="ORA-TABLE-OPTIONS",
                             message="Agrega TABLESPACE, COMPRESS, NOLOGGING y COMMENT en el DDL."))

    if policy.get("ORA-COL-PREFIX", True):
        cols = _columns(up)
        if cols:
            bad = [c for c in cols if not c.startswith(VALID_PREFIXES)]
            if bad:
                findings.append(dict(severity="MAJOR", rule_id="ORA-COL-PREFIX",
                                     message=("Usa prefijos estándar en columnas. Fechas ⇒ FH_, importes ⇒ IM_. Ej.: "
                                              + ", ".join(bad[:5]) + "...")))
    if policy.get("ORA-PK-IDX-NAMING", True) and _has_create_table(up):
        if " PRIMARY KEY " in up and " PK_" not in up:
            findings.append(dict(severity="MINOR", rule_id="ORA-PK-IDX-NAMING",
                                 message="Nombra PK/índice iniciando con PK_ e IDX_."))
    return findings
