from .models import User
from django.contrib.auth.hashers import check_password

def check_register_user(email, username):
    errors = {}
    if email:
        existing_user_email = User.objects.filter(email=email).first()
    if username:
        existing_user_username = User.objects.filter(username=username).first()
    if email and existing_user_email:
        errors['email'] = {'unique': f'{existing_user_email.email} is already in use'}
    if username and existing_user_username:
        errors['username'] = {'unique': f'{existing_user_username.username} is already in use'}
    return errors


def check_login_user(email_or_username, password):
    errors = {}
    try:
        existing_user = User.objects.get(email=email_or_username)
    except User.DoesNotExist:
        existing_user = User.objects.filter(username=email_or_username).first()
    if existing_user:
        if not check_password(password, existing_user.password):
            errors['password'] = {'validation': 'Password is incorrect'}
    else:
        errors['email_or_username'] = {'exists': 'User not found'}
    return errors

