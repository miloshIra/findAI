from wtforms.validators import ValidationError
from models import User

def ensure_existing_password_matches(form, field):
    """
    Ensures that the current password matches the existing password

    :param form: wtforms Instance
    :param field: Field being passed in
    :return: None 
    """

    user = User.query.get(form._obj.id)

    if not user.authendicated(password=field.data):
        raise ValidationError('Password does not match')