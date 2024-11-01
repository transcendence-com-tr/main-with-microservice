from django.urls import re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    re_path(r'^$', serve, {'path': 'index.html', 'document_root': settings.STATICFILES_DIRS[0]}),
    re_path(r'^(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS[0]}),
]
