from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TriplumRegisterView, TriplumUserDetailView

urlpatterns = [
	path('register/', TriplumRegisterView.as_view(), name='register'),
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('user/', TriplumUserDetailView.as_view(), name='user-detail'),
]
