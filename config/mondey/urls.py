from django.conf.urls import url
from .views import UserAPI, PushMessageAPI, TokenAPI, CustomCategoryView, ExpenditureView, IncomeHistoryView, CategoryHistoryView

urlpatterns = [
    url(r'user/', UserAPI.as_view(), name='user'),
    url(r'token/refresh/', TokenAPI.as_view(), name='token'),
    url(r'push/', PushMessageAPI.as_view(), name='push'),

    url(r'custom_category/', CustomCategoryView.as_view(), name='custom_category'),
    url(r'expenditure/', ExpenditureView.as_view(), name='expenditure'),
    url(r'income_history/', IncomeHistoryView.as_view(), name='income_history'),
    url(r'category_history/', CategoryHistoryView.as_view(), name='category_history'),
]
