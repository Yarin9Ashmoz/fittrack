from backend.app.services.user_service import UserService
from backend.app.utils.permissions import is_admin
from backend.app import exceptions


class AdminService(UserService):
    def __init__(self, session=None, current_user=None):
        super().__init__(session=session, current_user=current_user)
        # Optionally validate that current_user has admin rights
        if current_user and not is_admin(current_user):
            raise exceptions.PermissionError("Admin role required")

    @property
    def role_name(self) -> str:
        return "admin"

    # Admin specific helper
    def get_unresolved_error_reports(self):
        # Placeholder for admin-specific aggregated data
        # Real implementation would call ErrorReportRepository
        return []
