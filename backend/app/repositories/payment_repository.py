from .base_repository import BaseRepository
from ..models.payment import Payment

class PaymentRepository(BaseRepository[Payment]):
    def __init__(self, session):
        super().__init__(Payment, session)

    def get_by_member(self, member_id: int):
        from .subscription_repository import SubscriptionRepository
        # Simple implementation: find all subscriptions for member, then all payments for those
        sub_repo = SubscriptionRepository(self.session)
        subs = sub_repo.get_by_user(member_id)
        sub_ids = [s.id for s in subs]
        if not sub_ids:
            return []
        
        return self.session.query(Payment).filter(Payment.subscription_id.in_(sub_ids)).all()
