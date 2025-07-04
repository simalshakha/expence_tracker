from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT auth endpoints
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Django built-in auth views for session login/logout (browsable API)
    path('accounts/', include('django.contrib.auth.urls')),  # <-- add this line
    
    # Redirect root to /api/
    path('', RedirectView.as_view(url='/api/', permanent=False)), 
    
    # Your API urls
    path('api/', include('api.urls')),
]
