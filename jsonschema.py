#!/usr/bin/env python3


def validate(data, schema) -> tuple[bool, str]:
    def type_matches(value, expected_type: str) -> bool:
        if expected_type == "string":
            return isinstance(value, str)
        if expected_type == "integer":
            return isinstance(value, int) and not isinstance(value, bool)
        if expected_type == "number":
            return (isinstance(value, int) and not isinstance(value, bool)) or isinstance(value, float)
        if expected_type == "boolean":
            return isinstance(value, bool)
        if expected_type == "array":
            return isinstance(value, list)
        if expected_type == "object":
            return isinstance(value, dict)
        return False

    def _validate(value, rule, path: str):
        expected_type = rule.get("type")
        if expected_type and not type_matches(value, expected_type):
            return False, f"{path} should be {expected_type}"

        if expected_type == "object":
            required = rule.get("required", [])
            for field in required:
                if field not in value:
                    return False, f"{path}.{field} is required"

            properties = rule.get("properties", {})
            for field, field_rule in properties.items():
                if field in value:
                    ok, err = _validate(value[field], field_rule, f"{path}.{field}")
                    if not ok:
                        return False, err

        return True, ""

    return _validate(data, schema, "data")
