from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # All new API endpoints.
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),

]