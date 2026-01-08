from backend.app.db.database import SessionLocal
from backend.app.repositories.personal_tracking_repository import PersonalTrackingRepository
from backend.app import exceptions
from datetime import datetime, timedelta

def create_tracking_entry(tracking_data):
    """Create a new personal tracking entry"""
    with SessionLocal() as session:
        repo = PersonalTrackingRepository(session)
        return repo.create(**tracking_data.dict())

def get_tracking_entry_by_id(tracking_id: int):
    """Get tracking entry by ID"""
    with SessionLocal() as session:
        tracking = PersonalTrackingRepository(session).get_by_id(tracking_id)
        if not tracking:
            raise exceptions.NotFoundError("Tracking entry not found")
        return tracking

def get_tracking_by_member(member_id: int):
    """Get all tracking entries for a member"""
    with SessionLocal() as session:
        return PersonalTrackingRepository(session).get_by_member_id(member_id)

def get_tracking_by_date_range(member_id: int, start_date: datetime, end_date: datetime):
    """Get tracking entries for a member within a date range"""
    with SessionLocal() as session:
        return PersonalTrackingRepository(session).get_by_date_range(
            member_id, start_date, end_date
        )

def get_tracking_summary(member_id: int, days: int = 30):
    """Get summary of tracking for the last N days"""
    with SessionLocal() as session:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        entries = PersonalTrackingRepository(session).get_by_date_range(
            member_id, start_date, end_date
        )
        
        # Basic summary - can be enhanced with trend analysis
        return {
            "member_id": member_id,
            "period_days": days,
            "total_entries": len(entries),
            "entries": entries
        }

def update_tracking_entry(tracking_id: int, tracking_data):
    """Update an existing tracking entry"""
    with SessionLocal() as session:
        repo = PersonalTrackingRepository(session)
        update_data = {k: v for k, v in tracking_data.dict().items() if v is not None}
        updated = repo.update(tracking_id, **update_data)
        if not updated:
            raise exceptions.NotFoundError("Tracking entry not found")
        return updated
