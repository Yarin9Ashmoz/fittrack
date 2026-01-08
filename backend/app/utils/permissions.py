"""
Permission utilities for role-based access control.
Implements the permission model:
- Member: sees only their own data
- Trainer: sees their own data + their students' data
- Admin: sees everything
"""

def is_admin(user) -> bool:
    """Check if user is admin"""
    return user and user.role == "admin"

def is_trainer(user) -> bool:
    """Check if user is trainer"""
    return user and user.role == "trainer"

def is_member(user) -> bool:
    """Check if user is member"""
    return user and user.role == "member"

def can_view_user(current_user, target_user_id: int) -> bool:
    """
    Check if current user can view target user's data.
    - Admin: can view all
    - Trainer: can view their students
    - Member: can view only themselves
    """
    if is_admin(current_user):
        return True
    
    if is_member(current_user):
        return current_user.id == target_user_id
    
    if is_trainer(current_user):
        # Trainer can view themselves and their students
        if current_user.id == target_user_id:
            return True
        # TODO: Check if target_user is trainer's student
        # This would require checking enrollments where trainer teaches the class
        return False
    
    return False

def can_view_class(current_user, class_id: int) -> bool:
    """
    Check if current user can view class details.
    - Admin: can view all classes
    - Trainer: can view classes they teach
    - Member: can view classes they're enrolled in
    """
    if is_admin(current_user):
        return True
    
    # For trainer and member, would need to check class_sessions and enrollments
    # Placeholder for now
    return True

def can_view_payment(current_user, payment) -> bool:
    """
    Check if current user can view payment details.
    - Admin: can view all payments
    - Trainer: can view payments for their students
    - Member: can view only their own payments
    """
    if is_admin(current_user):
        return True
    
    if is_member(current_user):
        return payment.member_id == current_user.id
    
    if is_trainer(current_user):
        # Trainer can view their own payments and their students' payments
        if payment.member_id == current_user.id:
            return True
        # TODO: Check if payment.member_id is trainer's student
        return False
    
    return False

def can_manage_errors(current_user) -> bool:
    """Only admins can manage error reports"""
    return is_admin(current_user)

def can_create_intake_evaluation(current_user) -> bool:
    """Admin and trainers can create intake evaluations"""
    return is_admin(current_user) or is_trainer(current_user)

def can_view_personal_tracking(current_user, member_id: int) -> bool:
    """
    Check if current user can view personal tracking data.
    - Admin: can view all
    - Trainer: can view their students'
    - Member: can view only their own
    """
    if is_admin(current_user):
        return True
    
    if is_member(current_user):
        return current_user.id == member_id
    
    if is_trainer(current_user):
        # Trainer can view themselves and their students
        if current_user.id == member_id:
            return True
        # TODO: Check if member is trainer's student
        return False
    
    return False

def filter_users_by_permission(current_user, users_list):
    """
    Filter users list based on current user's permissions.
    - Admin: sees all users
    - Trainer: sees themselves + their students
    - Member: sees only themselves
    """
    if is_admin(current_user):
        return users_list
    
    if is_member(current_user):
        return [u for u in users_list if u.id == current_user.id]
    
    if is_trainer(current_user):
        # TODO: Filter to show trainer and their students
        # For now, just return the trainer themselves
        return [u for u in users_list if u.id == current_user.id]
    
    return []

def filter_classes_by_permission(current_user, classes_list):
    """
    Filter classes based on permissions.
    - Admin: sees all
    - Trainer: sees classes they teach
    - Member: sees classes they're enrolled in or can enroll in
    """
    if is_admin(current_user):
        return classes_list
    
    if is_trainer(current_user):
        # Filter to classes where current_user is trainer
        return [c for c in classes_list if c.trainer_id == current_user.id]
    
    # Members see all available classes (they can choose what to enroll in)
    return classes_list

def filter_payments_by_permission(current_user, payments_list):
    """
    Filter payments based on permissions.
    - Admin: sees all
    - Trainer: sees their own + their students'
    - Member: sees only their own
    """
    if is_admin(current_user):
        return payments_list
    
    if is_member(current_user):
        return [p for p in payments_list if p.member_id == current_user.id]
    
    if is_trainer(current_user):
        # TODO: Include students' payments
        return [p for p in payments_list if p.member_id == current_user.id]
    
    return []
