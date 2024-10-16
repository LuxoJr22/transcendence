from django.urls import path
from .views import ShooterMatchHistoryView, ShooterMatchMakingView, ShooterSettingsView

urlpatterns = [
	path('shooter/history/<int:user_id>/', ShooterMatchHistoryView.as_view(), name='shooter_history'),
	path('shooter/settings/<int:user_id>/', ShooterSettingsView.as_view(), name='players_settings'),
	path('shooter/create/', ShooterMatchMakingView.as_view(), name='shooter_create_game'),
]
