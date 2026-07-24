from django.urls import path

from .views import (
    index,
    TaskTypeListView,
    TaskTypeCreateView,
    PositionListView,
    PositionCreateView,
)


urlpatterns = [
    path("", index, name="index"),
    path("task-types/", TaskTypeListView.as_view(), name="tasktype-list"),
    path(
        "task-types/create/",
        TaskTypeCreateView.as_view(),
        name="tasktype-create"
    ),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
]

app_name = "task_manager"
