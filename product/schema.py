"""A small JSON-Schema subset validator (type, required, properties, items, enum, min/max items,
additionalProperties) — enough to hold every reasoning output to its contract without a dependency."""
from __future__ import annotations

_TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "integer": int, "number": (int, float),
          "null": type(None)}


def errors(value, schema: dict, path: str = "$") -> list[str]:
    out: list[str] = []
    t = schema.get("type")
    if t is not None:
        ts = t if isinstance(t, list) else [t]
        ok = False
        for one in ts:
            py = _TYPES[one]
            if isinstance(value, py) and not (one in ("integer", "number") and isinstance(value, bool)):
                ok = True
        if not ok:
            return [f"{path}: expected {t}, got {type(value).__name__}"]
    if "enum" in schema and value not in schema["enum"]:
        out.append(f"{path}: {value!r} not in {schema['enum']}")
    if isinstance(value, dict):
        for k in schema.get("required", []):
            if k not in value:
                out.append(f"{path}: missing required '{k}'")
        props = schema.get("properties", {})
        for k, v in value.items():
            if k in props:
                out += errors(v, props[k], f"{path}.{k}")
            elif schema.get("additionalProperties") is False:
                out.append(f"{path}: unexpected property '{k}'")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            out.append(f"{path}: fewer than {schema['minItems']} items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            out.append(f"{path}: more than {schema['maxItems']} items")
        if "items" in schema:
            for i, v in enumerate(value):
                out += errors(v, schema["items"], f"{path}[{i}]")
    if isinstance(value, str) and "maxLength" in schema and len(value) > schema["maxLength"]:
        out.append(f"{path}: longer than {schema['maxLength']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            out.append(f"{path}: below {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            out.append(f"{path}: above {schema['maximum']}")
    return out


def strict(schema: dict) -> dict:
    """The same schema with additionalProperties:false and every property required (structured-output form)."""
    if not isinstance(schema, dict):
        return schema
    s = dict(schema)
    if s.get("type") == "object" and "properties" in s:
        s["properties"] = {k: strict(v) for k, v in s["properties"].items()}
        s["additionalProperties"] = False
        s["required"] = list(s["properties"].keys())
    if "items" in s:
        s["items"] = strict(s["items"])
    for k in ("minimum", "maximum", "maxLength", "minItems", "maxItems"):
        s.pop(k, None) if k in ("maxLength",) else None
    return s
