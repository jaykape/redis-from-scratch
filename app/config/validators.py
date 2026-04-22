def validate_yes_no(value: str) -> str:
    if value not in ("yes", "no"):
        raise ValueError(f"Invalid value '{value}': must be 'yes' or 'no'")
    return value


def validate_non_empty(value: str) -> str:
    if not value.strip():
        raise ValueError("Value must not be empty")
    return value
