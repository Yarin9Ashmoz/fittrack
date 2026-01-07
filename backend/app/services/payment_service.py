from backend.app.db.database import SessionLocal
from backend.app.repositories.payment_repository import PaymentRepository
from backend.app import exceptions

def create_payment(data):
    with SessionLocal() as session:
        return PaymentRepository(session).create(**data.dict())

def get_payment_by_id(payment_id: int):
    with SessionLocal() as session:
        payment = PaymentRepository(session).get_by_id(payment_id)
        if not payment:
            raise exceptions.NotFoundError("Payment not found")
        return payment

def get_all_payments():
    with SessionLocal() as session:
        return PaymentRepository(session).get_all()

def get_payment_by_member(member_id: int):
    with SessionLocal() as session:
        return PaymentRepository(session).get_by_member(member_id)

def cancel_payment(payment_id: int):
    with SessionLocal() as session:
        repo = PaymentRepository(session)
        if not repo.get_by_id(payment_id):
            raise exceptions.NotFoundError("Payment not found")
        return repo.update(payment_id, status="canceled")

def update_payment(payment_id: int, data):
    with SessionLocal() as session:
        update_data = {k: v for k, v in data.dict().items() if v is not None}
        updated = PaymentRepository(session).update(payment_id, **update_data)
        if not updated:
            raise exceptions.NotFoundError("Payment not found")
        return updated

def delete_payment(payment_id: int):
    with SessionLocal() as session:
        if not PaymentRepository(session).delete(payment_id):
            raise exceptions.NotFoundError("Payment not found")
        return True
