from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('cmdb/', include('cmdb.urls')),
    path('admin/', admin.site.urls),
]