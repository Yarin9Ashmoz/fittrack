from backend.app.db.database import SessionLocal
from backend.app.repositories.payment_repository import PaymentRepository
from backend.app.repositories.class_session_repository import ClassSessionRepository
from backend.app.repositories.user_repository import UserRepository
from backend.app import exceptions
from decimal import Decimal
from datetime import datetime

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

def calculate_payment_for_closed_class(class_id: int, trainer_id: int, amount_per_session: float = 50.0):
    """
    Calculate payment for a trainer when a class is closed.
    This function is called automatically when class status changes to 'closed'.
    """
    with SessionLocal() as session:
        class_repo = ClassSessionRepository(session)
        payment_repo = PaymentRepository(session)
        
        cls = class_repo.get_by_id(class_id)
        if not cls:
            raise exceptions.NotFoundError("Class not found")
        
        if cls.status != "closed":
            raise exceptions.BadRequestError("Class must be closed to calculate payment")
        
        # Check if payment already exists for this class
        existing = session.query(payment_repo.model).filter(
            payment_repo.model.class_session_id == class_id,
            payment_repo.model.payment_method == "closed_lesson"
        ).first()
        
        if existing:
            raise exceptions.DuplicateError("Payment already calculated for this class")
        
        # Create payment for trainer
        calculated_amount = Decimal(str(amount_per_session))
        payment = payment_repo.create(
            member_id=trainer_id,
            payment_method="closed_lesson",
            class_session_id=class_id,
            calculated_amount=calculated_amount,
            discount_applied=Decimal("0.00"),
            amount=float(calculated_amount),
            status="pending"
        )
        
        return payment

def process_subscription_payment(subscription_id: int, amount: float):
    """
    Process monthly subscription payment.
    Called automatically or manually for recurring subscriptions.
    """
    with SessionLocal() as session:
        payment_repo = PaymentRepository(session)
        
        # Get member from subscription (would need subscription repository)
        # For now, require member_id to be passed
        
        calculated_amount = Decimal(str(amount))
        payment = payment_repo.create(
            member_id=0,  # TODO: Get from subscription
            payment_method="subscription",
            subscription_id=subscription_id,
            calculated_amount=calculated_amount,
            discount_applied=Decimal("0.00"),
            amount=float(calculated_amount),
            status="pending"
        )
        
        return payment

def mark_payment_as_paid(payment_id: int):
    """Mark a payment as completed"""
    with SessionLocal() as session:
        repo = PaymentRepository(session)
        payment = repo.get_by_id(payment_id)
        if not payment:
            raise exceptions.NotFoundError("Payment not found")
        
        updated = repo.update(
            payment_id,
            status="paid",
            paid_at=datetime.now()
        )
        return updated

def get_pending_payments():
    """Get all pending payments (admin view)"""
    with SessionLocal() as session:
        repo = PaymentRepository(session)
        return session.query(repo.model).filter(
            repo.model.status == "pending"
        ).all()
