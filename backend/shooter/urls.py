from django.urls import path
from .views import ShooterMatchMakingView

urlpatterns = [
	path('shooter/create/', ShooterMatchMakingView.as_view(), name='shooter_create_game'),
]
