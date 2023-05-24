from functools import wraps
from flask_login import current_user
from flask import flash, redirect


def role_required(*roles):
    """
    Checks user role for access permission.

    :param *roles: 1 or more allowed roles
    :return: Function
    """
    def decorator(func):
        @wraps(func)
        def decorator_function(*args, **kwargs):
            if current_user.role not in roles:
                flash('You dont have permission to do that', 'error')
                return redirect('/')
            return func(*args, **kwargs)
        return decorator_function
    return decorator
            