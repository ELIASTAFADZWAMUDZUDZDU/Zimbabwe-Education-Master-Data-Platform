"""Safety checks for SQL written by a language model.

The model's output is untrusted text, so it is checked before it reaches the
database. This is one layer of protection. The database connection is also
opened read-only (see ai_engine.execute_sql), and the best setup also uses a
database role that can only SELECT from the view.
"""
import re

ALLOWED_RELATION = "vw_school_directory"
MAX_ROWS = 500

FORBIDDEN_WORDS = (
    "insert", "update", "delete", "drop", "alter", "truncate", "create",
    "grant", "revoke", "copy", "into", "execute", "call", "do", "vacuum",
    "set", "reset", "lock", "listen", "notify", "union", "intersect", "except",
)
FORBIDDEN_PREFIXES = ("pg_", "lo_", "dblink", "information_schema")

_STRING_LITERAL = re.compile(r"'(?:[^']|'')*'")
_RELATION_AFTER_FROM_OR_JOIN = re.compile(r"\b(?:from|join)\s+([^\s,;()]+)")


def check_sql(sql):
    """Return (is_safe, reason). The reason is empty when the SQL is safe."""
    if not isinstance(sql, str) or not sql.strip():
        return False, "Empty query."

    text = sql.strip()

    if "--" in text or "/*" in text or "*/" in text:
        return False, "Comments are not allowed."
    if '"' in text or "\\" in text:
        return False, "Quoted identifiers and backslashes are not allowed."

    # Judge the structure only. String values such as ILIKE '%do%' are harmless.
    structure = _STRING_LITERAL.sub("''", text).lower()
    structure = re.sub(r"\s+", " ", structure).strip()

    if structure.endswith(";"):
        structure = structure[:-1].strip()
    if ";" in structure:
        return False, "Only one statement is allowed."

    if not structure.startswith("select "):
        return False, "Only SELECT queries are allowed."

    for word in FORBIDDEN_WORDS:
        if re.search(rf"\b{word}\b", structure):
            return False, f"'{word}' is not allowed."
    for prefix in FORBIDDEN_PREFIXES:
        if re.search(rf"\b{re.escape(prefix)}", structure):
            return False, f"'{prefix}' is not allowed."

    relations = _RELATION_AFTER_FROM_OR_JOIN.findall(structure)
    if not relations:
        return False, f"The query must read from {ALLOWED_RELATION}."
    if any(r != ALLOWED_RELATION for r in relations):
        return False, f"Only {ALLOWED_RELATION} may be queried."
    if re.search(r"\bfrom\s+\w+\s*,", structure):
        return False, "Multiple tables in FROM are not allowed."

    return True, ""


def validate_sql(sql):
    """True if the SQL passes every check."""
    return check_sql(sql)[0]


def prepare_sql(sql, max_rows=MAX_ROWS):
    """Validate the SQL and cap the number of rows it can return.

    Raises ValueError if the SQL is unsafe.
    """
    ok, reason = check_sql(sql)
    if not ok:
        raise ValueError(f"Unsafe SQL rejected: {reason}")
    body = sql.strip().rstrip(";").strip()
    return f"SELECT * FROM ({body}) AS limited_result LIMIT {int(max_rows)}"
