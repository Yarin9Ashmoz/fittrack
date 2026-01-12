from backend.app.services import checkin_service
import types


class DummySubscription:
    def __init__(self):
        self.id = 1
        self.status = 'active'
        self.remaining_entries = None
        self.debt = 0


class DummyUser:
    def __init__(self):
        self.id = 10
        self.first_name = 'Test'
        self.last_name = 'User'


class DummyRepo:
    def __init__(self, session):
        pass

    def get_active_by_user(self, member_id):
        return DummySubscription()

    def create(self, **kwargs):
        # return kwargs so caller can inspect
        return types.SimpleNamespace(**kwargs)


def test_create_checkin_sets_member_name(monkeypatch):
    created = {}

    # Patch repositories used inside create_checkin
    monkeypatch.setattr(checkin_service, 'SubscriptionRepository', lambda session: types.SimpleNamespace(get_active_by_user=lambda mid: DummySubscription()))
    monkeypatch.setattr(checkin_service, 'EnrollmentRepository', lambda session: types.SimpleNamespace(get_active_by_class=lambda cid: []))
    monkeypatch.setattr(checkin_service, 'UserRepository', lambda session: types.SimpleNamespace(get_by_id=lambda mid: DummyUser()))

    # Intercept CheckinRepository.create
    def fake_create(**kwargs):
        created.update(kwargs)
        return types.SimpleNamespace(**kwargs)

    monkeypatch.setattr(checkin_service, 'CheckinRepository', lambda session: types.SimpleNamespace(create=lambda **kw: fake_create(**kw)))

    result = checkin_service.create_checkin(10)

    assert 'member_name' in created
    assert created['member_name'] == 'Test User'
    assert result.member_name == 'Test User'
