"""String formatting utilities."""


def format_currency(amount: float, currency: str = "₪") -> str:
    """Format amount as currency.
    
    Args:
        amount: Amount to format
        currency: Currency symbol (default: ₪)
        
    Returns:
        Formatted currency string
    """
    return f"{currency}{amount:,.2f}"


def format_phone_display(phone: str) -> str:
    """Format phone number for display.
    
    Args:
        phone: Phone number string
        
    Returns:
        Formatted phone (e.g., 050-1234567)
    """
    clean = phone.replace("-", "").replace(" ", "")
    if len(clean) == 10:
        return f"{clean[:3]}-{clean[3:]}"
    return phone


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncate text with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add (default: ...)
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
