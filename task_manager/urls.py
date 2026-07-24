from django.urls import path

from .views import (
    index,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeDeleteView,
    PositionListView,
    PositionCreateView,
    PositionDeleteView,
)


urlpatterns = [
    path("", index, name="index"),
    path("task-types/", TaskTypeListView.as_view(), name="tasktype-list"),
    path(
        "task-types/create/",
        TaskTypeCreateView.as_view(),
        name="tasktype-create"
    ),
    path(
        "task-types/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="tasktype-delete"
    ),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
    path(
        "positions/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete"
    ),
]

app_name = "task_manager"
