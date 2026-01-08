from backend.app.repositories.base_repository import BaseRepository
from backend.app.models.personal_tracking import PersonalTracking
from sqlalchemy.orm import Session
from datetime import datetime

class PersonalTrackingRepository(BaseRepository[PersonalTracking]):
    def __init__(self, session: Session):
        super().__init__(PersonalTracking, session)
    
    def get_by_member_id(self, member_id: int):
        """Get all tracking entries for a specific member"""
        return self.session.query(self.model).filter(
            self.model.member_id == member_id
        ).order_by(self.model.tracking_date.desc()).all()
    
    def get_by_date_range(self, member_id: int, start_date: datetime, end_date: datetime):
        """Get tracking entries for a member within a date range"""
        return self.session.query(self.model).filter(
            self.model.member_id == member_id,
            self.model.tracking_date >= start_date,
            self.model.tracking_date <= end_date
        ).order_by(self.model.tracking_date.asc()).all()
