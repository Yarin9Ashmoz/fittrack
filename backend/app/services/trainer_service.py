from backend.app.services.user_service import UserService
from backend.app.utils.permissions import is_trainer
from backend.app import exceptions


class TrainerService(UserService):
    def __init__(self, session=None, current_user=None):
        super().__init__(session=session, current_user=current_user)
        if current_user and not is_trainer(current_user):
            raise exceptions.PermissionError("Trainer role required")

    @property
    def role_name(self) -> str:
        return "trainer"

    # Trainer-specific behavior
    def create_class_session(self, **data):
        # Implementation should call ClassSessionRepository
        # Placeholder implementation
        return {"created": True, "data": data}

    def get_my_classes(self):
        # Would query class sessions where trainer_id == current_user.id
        return []
