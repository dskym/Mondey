from django.conf.urls import url
from .views import UserList, TestList, PushList, TokenList

urlpatterns = [
    url(r'user/', UserList.as_view(), name='user'),
    url(r'token/refresh/', TokenList.as_view(), name='token'),
    url(r'test/', TestList.as_view(), name='test'),
    url(r'push/', PushList.as_view(), name='push'),
]
