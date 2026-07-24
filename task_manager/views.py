from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, TaskType, Position


@login_required
def index(request):
    num_user_tasks = request.user.tasks.count()
    num_tasks = Task.objects.count()
    context = {
        "num_user_tasks": num_user_tasks,
        "num_tasks": num_tasks,
    }
    return render(
        request,
        "task_manager/index.html",
        context=context
    )


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tasktype-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")
