"""Validation utility functions."""
import re


def validate_phone(phone: str) -> bool:
    """Validate Israeli phone number.
    
    Args:
        phone: Phone number string
        
    Returns:
        True if valid Israeli phone number
    """
    # Israeli phone: 05X-XXXXXXX or 0X-XXXXXXX
    pattern = r"^0(5[0-9]|[2-4]|[8-9])-?\d{7}$"
    return bool(re.match(pattern, phone.replace("-", "")))


def validate_email(email: str) -> bool:
    """Validate email address.
    
    Args:
        email: Email string
        
    Returns:
        True if valid email format
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def sanitize_string(text: str, max_length: int = 255) -> str:
    """Clean and limit string length.
    
    Args:
        text: Input text
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
    """
    # Remove extra whitespace
    cleaned = " ".join(text.split())
    # Limit length
    return cleaned[:max_length]
