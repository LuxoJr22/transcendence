from django.urls import path
from .views import TriplumRegisterView

urlpatterns = [
	path('register/', TriplumRegisterView.as_view(), name='register'),
]
