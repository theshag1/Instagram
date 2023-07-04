from django.urls import path
from user.views import UserApiview,  LoginApiView

urlpatterns = [
    path('profile/', UserApiview.as_view(), name='user'),
    path('login/', LoginApiView.as_view(), name='user-login')
]
