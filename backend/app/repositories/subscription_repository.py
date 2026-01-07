from .base_repository import BaseRepository
from ..models.subscription import Subscription

class SubscriptionRepository(BaseRepository[Subscription]):
    def __init__(self, session):
        super().__init__(Subscription, session)

    def get_active_by_user(self, user_id: int):
        return self.session.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.status == "active"
        ).first()

    def get_by_user(self, user_id: int):
        return self.session.query(Subscription).filter(Subscription.user_id == user_id).all()
