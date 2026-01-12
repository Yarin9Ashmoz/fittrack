from backend.app.services.service_factory import service_for_user
from backend.app.services.admin_service import AdminService
from backend.app.services.trainer_service import TrainerService
from backend.app.services.member_service import MemberService
from backend.app.services.user_service import UserService
import pytest


class DummyUser:
    def __init__(self, role, id=1):
        self.role = role
        self.id = id


def test_factory_returns_admin_service_for_admin():
    u = DummyUser(role='admin')
    svc = service_for_user(u)
    assert isinstance(svc, AdminService)


def test_factory_returns_trainer_service_for_trainer():
    u = DummyUser(role='trainer')
    svc = service_for_user(u)
    assert isinstance(svc, TrainerService)


def test_factory_returns_member_service_for_member():
    u = DummyUser(role='member')
    svc = service_for_user(u)
    assert isinstance(svc, MemberService)


def test_factory_returns_user_service_for_none():
    svc = service_for_user(None)
    assert isinstance(svc, UserService)


def test_user_service_is_abstract():
    from backend.app.services.user_service import UserService
    with pytest.raises(TypeError):
        UserService()


def test_admin_service_requires_admin_role():
    u = DummyUser(role='member')
    with pytest.raises(Exception):
        AdminService(current_user=u)
