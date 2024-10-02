from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, UserDetailView, UserUpdateView, UserProfileView, UserListView,UserSkinUpdateView, OAuth42RedirectView, OAuth42CallbackView

urlpatterns = [
	path('register/', RegisterView.as_view(), name='register'),
	path('login/', LoginView.as_view(), name='login'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('oauth42/', OAuth42RedirectView.as_view(), name='oauth42'),
	path('oauth42/callback/', OAuth42CallbackView.as_view(), name='oauth42_callback'),

	path('user/', UserDetailView.as_view(), name="user_detail"),
	path('user/profile/<int:id>/', UserProfileView.as_view(), name='user_profile'),
	path('user/list/', UserListView.as_view(), name='user_list'),
	path('user/update/', UserUpdateView.as_view(), name='user_update'),
	path('user/skin/update/', UserSkinUpdateView.as_view(), name='user_skin_update'),
]
