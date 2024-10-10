from django.urls import path
from .views import ShooterMatchMakingView, ShooterSettingsView

urlpatterns = [
	path('shooter/settings/<int:user_id>/', ShooterSettingsView.as_view(), name='players_settings'),
	path('shooter/create/', ShooterMatchMakingView.as_view(), name='shooter_create_game'),
]
