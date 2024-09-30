from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/', include('users.urls')),
	path('api/', include('friendship.urls')),
	path('api/', include('chat.urls')),
	path('api/', include('tournament.urls')),
	path('api/', include('pong.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
