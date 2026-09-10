"""A generic reader for the frozen contract YAMLs.

The contracts describe their objects as `fields: {name: {type, required, default, fields}}`.
This walks that description; it knows nothing about any particular contract, so a v1 field
is validated the day it is added and no code here is edited to add one.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from .errors import Refusal
from .util import load_yaml

_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?$")
_LIST = re.compile(r"^list\[(.+)\]$")


@dataclass(frozen=True)
class Contract:
    schema: str
    fields: dict
    source: str

    @classmethod
    def load(cls, path: str | Path) -> "Contract":
        doc = load_yaml(path) or {}
        return cls(schema=doc.get("schema", str(path)), fields=doc.get("fields", {}), source=str(path))

    def validate(self, obj: Any, *, code: str = Refusal.SCHEMA_VIOLATION) -> dict:
        """Return a normalised copy; raise Refusal on the first violation."""
        if not isinstance(obj, dict):
            raise Refusal(code, f"{self.schema} expects an object", got=type(obj).__name__)
        return _object(obj, self.fields, self.schema, "", code)


def _object(obj: dict, spec: dict, schema: str, prefix: str, code: str) -> dict:
    unknown = sorted(set(obj) - set(spec))
    if unknown:
        raise Refusal(
            code,
            f"{schema} has no field {prefix}{unknown[0]!r}; a v0 object never carries an undeclared key",
            schema=schema,
            unknown=unknown,
        )
    out: dict[str, Any] = {}
    for name, field in spec.items():
        where = f"{prefix}{name}"
        present = name in obj and obj[name] is not None
        if not present:
            if "default" in field:
                out[name] = field["default"]
            elif field.get("required") is True:
                raise Refusal(code, f"{schema} requires {where}", schema=schema, field=where)
            continue
        out[name] = _value(obj[name], field, schema, where, code)
    return out


def _value(value: Any, field: dict, schema: str, where: str, code: str) -> Any:
    declared = str(field.get("type", "string")).strip()
    inner = _LIST.match(declared)
    if inner:
        if not isinstance(value, list):
            raise Refusal(code, f"{where} must be a list", schema=schema, field=where, got=type(value).__name__)
        item_type = inner.group(1).strip()
        if item_type == "object":
            sub = field.get("fields")
            if sub is None:
                return [dict(v) for v in value]
            return [_object(_require_dict(v, where, schema, code), sub, schema, f"{where}[].", code) for v in value]
        return [_scalar(v, item_type, schema, f"{where}[]", code) for v in value]
    if declared == "object":
        sub = field.get("fields")
        value = _require_dict(value, where, schema, code)
        if sub is None:
            return dict(value)
        return _object(value, sub, schema, f"{where}.", code)
    return _scalar(value, declared, schema, where, code)


def _require_dict(value: Any, where: str, schema: str, code: str) -> dict:
    if not isinstance(value, dict):
        raise Refusal(code, f"{where} must be an object", schema=schema, field=where, got=type(value).__name__)
    return value


def _scalar(value: Any, declared: str, schema: str, where: str, code: str) -> Any:
    if declared == "string":
        if not isinstance(value, str) or value == "":
            raise Refusal(code, f"{where} must be a non-empty string", schema=schema, field=where, got=repr(value))
        return value
    if declared == "timestamp":
        if not isinstance(value, str) or not _TIMESTAMP.match(value):
            raise Refusal(code, f"{where} must be an ISO-8601 timestamp", schema=schema, field=where, got=repr(value))
        return value
    if declared == "int":
        if isinstance(value, bool) or not isinstance(value, int):
            raise Refusal(code, f"{where} must be an integer", schema=schema, field=where, got=repr(value))
        return value
    if declared == "number":
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise Refusal(code, f"{where} must be a number", schema=schema, field=where, got=repr(value))
        return value
    if declared == "bool":
        if not isinstance(value, bool):
            raise Refusal(code, f"{where} must be a boolean", schema=schema, field=where, got=repr(value))
        return value
    if declared == "decimal":
        try:
            dec = Decimal(str(value))
        except (InvalidOperation, ValueError):
            raise Refusal(code, f"{where} must be a decimal", schema=schema, field=where, got=repr(value)) from None
        # money is carried as an exact string, never as a float
        return format(dec, "f")
    raise Refusal(code, f"{where}: unsupported declared type {declared!r}", schema=schema, field=where)
