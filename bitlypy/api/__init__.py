from pydantic import ValidationError


def handle_validation_error(e: ValidationError):
    return f"Invalid request {e.errors()}", 400
