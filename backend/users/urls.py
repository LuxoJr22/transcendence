from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
	RegisterView,
	LoginView,
	UserDetailView,
	UserUpdateView,
	UserProfileView,
	UserListView,
	UserSkinUpdateView,
	SettingsUpdateView,
	OAuth42RedirectView,
	OAuth42CallbackView,
	QRCode2FAView,
	Enable2FAView,
	Disable2FAView,
	Verify2FAView,
)

urlpatterns = [
	path('register/', RegisterView.as_view(), name='register'),
	path('login/', LoginView.as_view(), name='login'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

	path('2fa/qrcode/', QRCode2FAView.as_view(), name='2fa_qrcode'),
	path('2fa/enable/', Enable2FAView.as_view(), name='2fa_enable'),
	path('2fa/disable/', Disable2FAView.as_view(), name='2fa_disable'),
	path('2fa/verify/', Verify2FAView.as_view(), name='2fa_verify'),

	path('oauth42/', OAuth42RedirectView.as_view(), name='oauth42'),
	path('oauth42/callback/', OAuth42CallbackView.as_view(), name='oauth42_callback'),

	path('user/', UserDetailView.as_view(), name="user_detail"),
	path('user/profile/<int:id>/', UserProfileView.as_view(), name='user_profile'),
	path('user/list/', UserListView.as_view(), name='user_list'),
	path('user/update/', UserUpdateView.as_view(), name='user_update'),
	path('user/skin/update/', UserSkinUpdateView.as_view(), name='user_skin_update'),
	path('user/settings/update/', SettingsUpdateView.as_view(), name='settings_update'),
]
