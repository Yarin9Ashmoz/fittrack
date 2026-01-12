from backend.app.services.user_service import UserService
from backend.app.utils.permissions import is_member
from backend.app import exceptions


class MemberService(UserService):
    def __init__(self, session=None, current_user=None):
        super().__init__(session=session, current_user=current_user)
        if current_user and not is_member(current_user):
            raise exceptions.PermissionError("Member role required")

    @property
    def role_name(self) -> str:
        return "member"

    # Member-specific behavior
    def create_personal_tracking(self, member_id: int, data: dict):
        # Would call PersonalTrackingRepository to create an entry
        return {"created": True, "member_id": member_id, "data": data}

    def get_my_subscriptions(self, member_id: int):
        # Would return subscriptions for the member
        return []
