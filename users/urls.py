from django.urls import path

from users.views import SignupView, UserInviteAPIView, UserInviteAcceptAPIView, UserInviteRefuseAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='user-signup'),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

    path('invite/', UserInviteAPIView.as_view(), name='user-invite'),
    path('invite/accept/', UserInviteAcceptAPIView.as_view(), name='user-accept'),
    path('invite/refuse/', UserInviteRefuseAPIView.as_view(), name='user-refuse'),
]
