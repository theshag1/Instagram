from django.urls import path

from .views import LoginUser, UserRegisterApi, LogoutUser, SendCodeForUpdateAPIView, CheckCodeSendAPIView, \
    Step4ForUpdatePasscode, User_Password_change, BasicUserView

urlpatterns = [
    path('', BasicUserView.as_view(), name='basic-view'),
    path('login/', LoginUser.as_view(), name='login-user'),
    path('logout/', LogoutUser.as_view(), name='login-user'),
    path('<str:username>/changepassword/', User_Password_change.as_view(), name='user'),
    path('register/', UserRegisterApi.as_view(), name='user-register'),
    path('forgotpassword/', SendCodeForUpdateAPIView.as_view(), name='user-forgot-passcode'),
    path('checksendcode/', CheckCodeSendAPIView.as_view(), name='check-send-code'),
    path('whaenuserdasiu32kiogbwqyfiwdfwuiefhwiuefhwodasoiewhfuvu23/', Step4ForUpdatePasscode.as_view(), name='URL'),

]
