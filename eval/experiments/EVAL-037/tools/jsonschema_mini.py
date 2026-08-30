#!/usr/bin/env python3
"""A dependency-free JSON Schema checker covering the subset EVAL-037's schemas use.

`jsonschema` is not installable in the execution environment (PEP 668), and an
execution lane must not have to install anything to validate its own evidence. This
covers exactly what schemas/*.json use and REFUSES anything it does not implement,
so a schema can never be silently under-validated:

  type, const, enum, pattern, required, properties, additionalProperties,
  items, minItems, maxItems, minimum, maximum, allOf, anyOf, not, if/then/else,
  $ref to #/$defs/*, $defs, description/title/$schema/$id/format/default (ignored)

`format` is accepted and NOT enforced - the same as jsonschema's default behaviour.
"""
import re

SUPPORTED = {
    "type", "const", "enum", "pattern", "required", "properties", "additionalProperties",
    "items", "minItems", "maxItems", "minimum", "maximum", "allOf", "anyOf", "not",
    "if", "then", "else", "$ref", "$defs", "$schema", "$id", "title", "description",
    "format", "default",
}

_TYPES = {"object": dict, "array": list, "string": str, "boolean": bool,
          "number": (int, float), "integer": int, "null": type(None)}


class SchemaUnsupported(RuntimeError):
    pass


def validate(instance, schema, root=None, path="$"):
    """Return a list of human-readable error strings. Empty list == valid."""
    root = root if root is not None else schema
    errs = []
    unknown = set(schema) - SUPPORTED
    if unknown:
        raise SchemaUnsupported(f"{path}: schema keywords not implemented: {sorted(unknown)}")

    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/$defs/"):
            raise SchemaUnsupported(f"{path}: only #/$defs/* refs are supported, got {ref}")
        return validate(instance, root["$defs"][ref.split("/")[-1]], root, path)

    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        py = tuple(t for name in types for t in
                   (_TYPES[name] if isinstance(_TYPES[name], tuple) else (_TYPES[name],)))
        ok = isinstance(instance, py)
        if ok and bool not in py and isinstance(instance, bool) and "boolean" not in types:
            ok = False  # bool is an int in Python; JSON Schema says it is not
        if not ok:
            return [f"{path}: expected type {types}, got {type(instance).__name__}"]

    if "const" in schema and instance != schema["const"]:
        errs.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errs.append(f"{path}: {instance!r} not in enum {schema['enum']}")
    if "pattern" in schema and isinstance(instance, str):
        if not re.search(schema["pattern"], instance):
            errs.append(f"{path}: {instance!r} does not match /{schema['pattern']}/")
    if "minimum" in schema and isinstance(instance, (int, float)) and instance < schema["minimum"]:
        errs.append(f"{path}: {instance} < minimum {schema['minimum']}")
    if "maximum" in schema and isinstance(instance, (int, float)) and instance > schema["maximum"]:
        errs.append(f"{path}: {instance} > maximum {schema['maximum']}")

    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errs.append(f"{path}: missing required property {key!r}")
        props = schema.get("properties", {})
        for k, v in instance.items():
            if k in props:
                errs += validate(v, props[k], root, f"{path}.{k}")
            elif schema.get("additionalProperties") is False:
                errs.append(f"{path}: additional property {k!r} is not allowed")

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errs.append(f"{path}: {len(instance)} items < minItems {schema['minItems']}")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errs.append(f"{path}: {len(instance)} items > maxItems {schema['maxItems']}")
        if "items" in schema:
            for i, item in enumerate(instance):
                errs += validate(item, schema["items"], root, f"{path}[{i}]")

    for sub in schema.get("allOf", []):
        errs += validate(instance, sub, root, path)
    if "anyOf" in schema:
        if all(validate(instance, sub, root, path) for sub in schema["anyOf"]):
            errs.append(f"{path}: matched no branch of anyOf")
    if "not" in schema and not validate(instance, schema["not"], root, path):
        errs.append(f"{path}: matched a schema it must not match")
    if "if" in schema:
        if not validate(instance, schema["if"], root, path):
            if "then" in schema:
                errs += validate(instance, schema["then"], root, path)
        elif "else" in schema:
            errs += validate(instance, schema["else"], root, path)
    return errs
