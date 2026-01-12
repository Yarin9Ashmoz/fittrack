from backend.app.utils.permissions import is_admin, is_trainer, is_member
from backend.app.services.admin_service import AdminService
from backend.app.services.trainer_service import TrainerService
from backend.app.services.member_service import MemberService
from backend.app.services.user_service import GenericUserService, UserService


def service_for_user(user, session=None):
    """Return appropriate service instance for the given user."""
    if not user:
        return GenericUserService(session=session, current_user=None)

    if is_admin(user):
        return AdminService(session=session, current_user=user)
    if is_trainer(user):
        return TrainerService(session=session, current_user=user)
    if is_member(user):
        return MemberService(session=session, current_user=user)

    # fallback to generic
    return GenericUserService(session=session, current_user=user)
