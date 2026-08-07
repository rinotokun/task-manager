from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("task_manager.urls", namespace="task_manager")),
    path("accounts/", include("django.contrib.auth.urls")),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    urlpatterns.append(
        path("__debug__/", include("debug_toolbar.urls"))
    )
