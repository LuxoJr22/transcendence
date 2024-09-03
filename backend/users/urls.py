from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, UserDetailView, UserUpdateView, UserProfileView

urlpatterns = [
	path('register/', RegisterView.as_view(), name='register'),
	path('login/', LoginView.as_view(), name='login'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('user/', UserDetailView.as_view(), name="user_detail"),
	path('user/update/', UserUpdateView.as_view(), name='user_update'),
	path('user/profile/<str:username>/', UserProfileView.as_view(), name='user_profile'),
]
