import jwt
from django.conf import settings
from django.urls import reverse
from .responses import error_response
from django.urls import resolve, Resolver404
from django.http import JsonResponse

class DisableCSRFMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response

class URLPathMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if not request.path.endswith('/'):
            request.path_info = request.path = f"{request.path}/"
        try:
            print(request.path_info)
            resolve(request.path_info)
        except Resolver404:
            return error_response("URL Error", "URL not found", "error",
                                   404, None, {'url': {'required': 'URL not found or in invalid format'}})
        return self.get_response(request)
    

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Token kontrolünü atlayacağımız URL'ler
        excluded_paths = [
            reverse('register'),  # Kendi URL adınıza göre güncelleyin
            reverse('login'),  # Kendi URL adınıza göre güncelleyin
            reverse('login_42'),  # Kendi URL adınıza göre güncelleyin
            reverse('login_42_callback'),  # Kendi URL adınıza göre güncelleyin
            '/favicon.ico',  # Favicon istekleri
        ]

        # `startswith` ile URL'in herhangi bir alt yolunu da dahil etmek için kontrol
        if any(request.path.startswith(path) for path in excluded_paths):
            return self.get_response(request)

        # Token kontrolü
        token = request.headers.get('Authorization')
        if token is None or not token.startswith('Bearer '):
            return error_response(
                "Token Error",
                "Unauthorized Token",
                "error",
                401,
                None,
                {
                    'token': {
                        'required': 'Token not provided or invalid'
                    }
                }
            )
        token = token.split(' ')[1]
        try:
            # Token'ı decode et
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            from .models import User
            request.user = User.objects.get(id=user_id)
            request.user.verify_code = payload.get('verify_code')
            request.user.password_code = payload.get('password_code')
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return error_response(
                "Token Error",
                "Unauthorized Token",
                "error",
                401,
                None,
                {
                    'token': {'required': 'Token expired or invalid'}
                }
            )

        response = self.get_response(request)
        return response
