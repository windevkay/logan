import re


def sanitize_input(input_string):
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    return re.sub(r'\W+', '', input_string)


def validate_json_fields(*args) -> bool:
    return all(arg is not None for arg in args)