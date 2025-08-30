# validators.py
import re
from pydantic import validator
from sqlmodel import SQLModel

def validate_username(cls, value: str) -> str:
    pattern = r"^(?!-)[A-Za-z0-9]+(-[A-Za-z0-9]+)*$"
    if not re.fullmatch(pattern, value):
        raise ValueError(
            "Username may only contain alphanumeric characters or single hyphens, and cannot begin or end with a hyphen."
        )
    return value

def validate_password(cls, value: str) -> str:
    errors = []
    if len(value) < 8:
        errors.append("contain at least 8 characters")
    if not re.search(r"[A-Z]", value):
        errors.append("contain at least one uppercase letter")
    if not re.search(r"[a-z]", value):
        errors.append("contain at least one lowercase letter")
    if not re.search(r"[0-9]", value):
        errors.append("contain at least one digit")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
        errors.append("contain at least one special character")

    if errors:
        raise ValueError("Password must " + ", ".join(errors) + ".")

    return value

def validate_email(cls, value: str) -> str:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.fullmatch(pattern, value):
        raise ValueError("Invalid email format.")
    blocked_domains = ["tempmail.com", "10minutemail.com"]
    domain = value.split("@")[1]
    if domain in blocked_domains:
        raise ValueError("Disposable email addresses are not allowed.")
    return value

class StripWhitespaceMixin(SQLModel):
    @validator("*", pre=True)
    def strip_strings(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value
