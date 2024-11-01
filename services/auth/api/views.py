from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from .models import User
from rest_framework.permissions import AllowAny
from .validations import RegisterValidator , LoginValidator , UpdateUserValidator , PasswordResetValidator , PasswordForgotValidator
from .checkers import check_register_user, check_login_user
from .responses import error_response, success_response
import jwt
from django.conf import settings
from django.core.mail import send_mail
import requests
import random
import time
from django.utils.crypto import get_random_string

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    validator = RegisterValidator({'username': username, 'email': email, 'password': password})
    status = validator.validate()
    if status:
        errors = check_register_user(email, username)
        if errors:
            return error_response("Register Error", "An error was encountered while registering", "error", 400, None,
                                  errors)
        hashed_password = make_password(password)
        user = User.objects.create(
            username=username,
            email=email,
            password=hashed_password
        )
        user.save()
        token = jwt.encode({
            "user_id": user.id,
        }, settings.SECRET_KEY, algorithm='HS256')
        print("register succeed")
        return success_response("Register Succeed", "Successfully registered", "success", 200, {
            "token": token
        }, None, True, "#/home")
    else:
        errors = validator.get_message()
        print(errors)
        return error_response("Register Error", "An error was encountered while registering", "error", 400, None,
                              errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    data = request.data
    email_or_username = data.get('email_or_username').strip()
    password = data.get('password')
    validator = LoginValidator({'email_or_username': email_or_username, 'password': password})
    status = validator.validate()
    if status:  
        errors = check_login_user(email_or_username, password)
        if errors:
            return error_response("Login Error", "An error was encountered while logging in", "error", 400, None,
                                  errors)
        else:
            try:
                user = User.objects.get(email=email_or_username)
            except User.DoesNotExist:
                user = User.objects.get(username=email_or_username)
            token = jwt.encode({
                "user_id": user.id,
            }, settings.SECRET_KEY, algorithm='HS256')
            print("login succeed")
            return success_response("Login Succeed", "Successfully logged in", "success", 200, {
                "token": token
            }, None, True, "#/home")
    else:
        errors = validator.get_message()
        print(errors)
        return error_response("Login Error", "An error was encountered while logging in",
                              "error", 400, None, errors)


@api_view(['GET'])
@permission_classes([AllowAny])
def me(request):
    return success_response("User Info", "User information is successfully fetched", "success", 200, {
        "user": {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "username_42": request.user.username_42,
            "email_42": request.user.email_42,
        }}, None, None)

@api_view(['GET'])
@permission_classes([AllowAny])
def login_42(request):
    return success_response("42 Login redirection", "You are redirecting to 42 login page", "success",
                            200, None, None, True,
                            "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-75f1e5c8c124aef4f03916acb167045d1e3df9603c571a9695b8aa116701abbb&redirect_uri=http%3A%2F%2Flocalhost%2F&response_type=code")

@api_view(['GET'])
@permission_classes([AllowAny])
def login_42_callback(request):
    code = request.GET.get('code')
    print(code)
    response = requests.post('https://api.intra.42.fr/oauth/token', data={
        'grant_type': 'authorization_code',
        'client_id': 'u-s4t2ud-75f1e5c8c124aef4f03916acb167045d1e3df9603c571a9695b8aa116701abbb',
        'client_secret': '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',
        'code': code,
        'redirect_uri': 'http://localhost/'
    })
    data = response.json()
    print(data)
    access_token = data.get('access_token')
    user_42 = requests.get('https://api.intra.42.fr/v2/me', headers={
        'Authorization': f'Bearer {access_token}'
    }).json()

    if (User.objects.filter(username_42=user_42.get('login')).exists()):
        user_id = User.objects.get(username_42=user_42.get('login')).id
        token = jwt.encode({
            "user_id": user_id,
            "iat": time.time(),
        }, settings.SECRET_KEY, algorithm='HS256')
        print("42 login succeed")
        return success_response("42 Login Succeed", "Successfully logged in with 42", "success", 200, {'token': token}, None, True, "#/home")
    else:
        user = User.objects.create(
            username_42=user_42.get('login'),
            email_42=user_42.get('email'),
            password=make_password(get_random_string(length=32)),
        )
        user.save()
        token = jwt.encode({
            "user_id": user.id,
        }, settings.SECRET_KEY, algorithm='HS256')
        return success_response("42 Login Succeed", "Successfully logged in with 42", "success", 200, {'token': token}, None, True, "#/home")

@api_view(['PUT'])
def auth(request):

    data = request.data
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    ## en son eklenen ! 
    if not request.user.email and not request.user.username:
        validator = PasswordResetValidator({'password': password})
        status = validator.validate()
        if not status:
            errors = validator.get_message()
            print(errors)
            return error_response("Update Error", "An error was encountered while updating", "error", 400, None, errors, False)
    
    if not email and not username:
        return error_response("Update Error", "At least one field must be provided", "error", 400, None, None, False, None)

    validator  = UpdateUserValidator({'email': email , 'username': username})
    status = validator.validate()
    if status:
            errors = check_register_user(email, username)
            if errors:
                return error_response("Update Error", "An error was encountered while updating", "error", 400, None, errors, False)

            if email and not User.objects.filter(email=email).exists():
                User.objects.filter(email=request.user.email).update(email=email)
            if username and not User.objects.filter(username=username).exists():
                User.objects.filter(username=request.user.username).update(username=username)
            
            ## en son eklenen ! 
            if not request.user.email and not request.user.username:
                hashed_password = make_password(password)
                User.objects.filter(id=request.user.id).update(password=hashed_password)
                
            return success_response("Update Succeed", "User successfully updated", "success", 200, None, None, True, "#/home")    
    else:
        errors = validator.get_message()
        print(errors)
        return error_response("Update Error", "An error was encountered while updating", "error", 400, None, errors, False)


@api_view(['POST'])
@permission_classes([AllowAny])
def two_factor(request):
    #random code 6 digit
    verify_code = random.randint(100000, 999999)

    token = jwt.encode({
        "user_id": request.user.id,
        'verify_code': str(verify_code),
        ## 10 dakika expire time
        "exp": time.time() + 600
    }, settings.SECRET_KEY, algorithm='HS256')

    email = request.user.email

    try: 
        send_mail(
            'Activate Your Account',
            'Activate your account with this code: ' + str(verify_code),
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
    except:
        return error_response("Email Verification Error", "Email could not be sent", "error", 400, None, None, True, None)

    return success_response("Email Verification Succeed", "Email verification sent successfully", "success", 200, {
        "token": token
    }, None, True, "#/home")


@api_view(['POST'])
@permission_classes([AllowAny])
def two_factor_verify(request):
    verify_code = request.data.get('verify_code')
    if (verify_code == request.user.verify_code):
        token = jwt.encode({
            "user_id": request.user.id,
            ## one month expire time
            "exp": time.time() + 2592000
        }, settings.SECRET_KEY, algorithm='HS256')
        return success_response("Verification Succeed", "Verification succeed", "success", 200, {
            "token": token
        }, None, True, "#/home")
    else:
        return error_response("Verification Error", "Verification failed", "error", 400, None, None, True, None)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_forgot(request):
    email_or_username = request.data.get('email_or_username')

    validator = PasswordForgotValidator({'email_or_username': email_or_username})
    status = validator.validate()

    if status:
        if ('@' in email_or_username):
            email = email_or_username
        else:
            username = email_or_username
            if (User.objects.filter(username=username).exists()):
                email = User.objects.get(username=username).email
            else:
                return error_response("Email Verification Error", "Username didn't find", "error", 400, None, None, True, None)

        if email and (User.objects.filter(email=email).exists()):
            password_code = random.randint(100000, 999999)
            token = jwt.encode({
                "user_id": request.user.id,
                'password_code': str(password_code),
                ## 10 dakika expire time
                "exp": time.time() + 600
            }, settings.SECRET_KEY, algorithm='HS256')
            send_mail(
                'Reset Password',
                'Reset your password with this code: ' + str(password_code),
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return success_response("Email Verification Succeed", "Email verification sent successfully", "success", 200, {
                "token": token
            }, None, True, "#/home")
    
        else:
            return error_response("Email Verification Error", "Email not found", "error", 400, None, None, True, None)
        
    else:
        errors = validator.get_message()
        print(errors)
        return error_response("Email Verification Error", "An error was encountered while sending email", "error", 400, None, errors)

    

@api_view(['PUT'])
@permission_classes([AllowAny])
def password_reset(request):
    password_code = request.data.get('password_code')
    password = request.data.get('password')

    validator = PasswordResetValidator({'password': password})
    status = validator.validate()

    if status:
        if (password_code == request.user.password_code):
            hashed_password = make_password(password)
            User.objects.filter(id=request.user.id).update(password=hashed_password)
            token = jwt.encode({
                "user_id": request.user.id,
                ## one month expire time
                "exp": time.time() + 2592000
            }, settings.SECRET_KEY, algorithm='HS256')
            return success_response("Password Reset Succeed", "Password reset succeed", "success", 200, {
                "token": token}, None, True, "#/home")
        else:
            return error_response("Password Reset Error", "Password code is invalid", "error", 400, None, None, True, None)
        
    else:
        errors = validator.get_message()
        print(errors)
        return error_response("Password Reset Error", "An error was encountered while resetting password", "error", 400, None, errors)


