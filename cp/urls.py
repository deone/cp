from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Customer-related URLs
    path('', include('customer.urls', namespace='customer')),
    # path('accounts/', include('django.contrib.auth.urls')),

    path('admin/', admin.site.urls),
]
