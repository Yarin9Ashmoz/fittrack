"""Date and time utility functions."""
from datetime import datetime, date, timedelta


def format_date(dt: date, format: str = "%Y-%m-%d") -> str:
    """Format date to string.
    
    Args:
        dt: Date to format
        format: Format string (default: YYYY-MM-DD)
        
    Returns:
        Formatted date string
    """
    return dt.strftime(format)


def days_between(start_date: date, end_date: date) -> int:
    """Calculate number of days between two dates.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        Number of days
    """
    return (end_date - start_date).days


def is_subscription_active(start_date: date, end_date: date) -> bool:
    """Check if subscription is currently active.
    
    Args:
        start_date: Subscription start date
        end_date: Subscription end date
        
    Returns:
        True if subscription is active
    """
    today = date.today()
    return start_date <= today <= end_date


def add_months(source_date: date, months: int) -> date:
    """Add months to a date.
    
    Args:
        source_date: Starting date
        months: Number of months to add
        
    Returns:
        New date
    """
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, [31, 29 if year % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return date(year, month, day)
