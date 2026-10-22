from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # All new API endpoints.
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),

]