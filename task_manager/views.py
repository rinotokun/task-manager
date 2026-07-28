from django.contrib.auth.decorators import login_required
from django.db.models import Count, Case, Value, When
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, TaskType, Position
from .forms import TaskForm


@login_required
def index(request):
    date_today = timezone.now().date()
    num_tasks = Task.objects.count()
    completed = Task.objects.filter(is_completed=True).count()
    overdue = Task.objects.filter(
        deadline__lt=date_today,
        is_completed=False
    ).count()
    upcoming_deadlines = Task.objects.filter(
        is_completed=False
    ).order_by("deadline")[:5]
    tasks_by_priority = Task.objects.values(
        "priority"
    ).annotate(
        count=Count("id"),
        priority_level=Case(
            When(priority=Task.Priority.URGENT, then=Value(1)),
            When(priority=Task.Priority.HIGH, then=Value(2)),
            When(priority=Task.Priority.MEDIUM, then=Value(3)),
            When(priority=Task.Priority.LOW, then=Value(4))
        )
    ).order_by("priority_level")
    context = {
        "num_tasks": num_tasks,
        "completed": completed,
        "in_progress": num_tasks - completed,
        "overdue": overdue,
        "date_today": date_today.strftime("%A, %d %B %Y"),
        "upcoming_deadlines": upcoming_deadlines,
        "tasks_by_priority": tasks_by_priority,
    }
    return render(
        request,
        "task_manager/index.html",
        context=context
    )


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_queryset(self):
        queryset = Task.objects.select_related(
            "task_type"
        ).prefetch_related("assignees")
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_queryset(self):
        queryset = Task.objects.select_related(
            "task_type"
        ).prefetch_related("assignees")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_url"] = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:task-list")
        )
        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        current_task_id = self.object.pk
        return reverse_lazy(
            "task_manager:task-detail",
            kwargs={"pk": current_task_id}
        )


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:task-list")
        )
        return context


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    queryset = TaskType.objects.prefetch_related("tasks")
    paginate_by = 5


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tasktype-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:tasktype-list")
        )
        return context


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tasktype-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:tasktype-list")
        )
        return context


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:tasktype-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:tasktype-list")
        )
        return context


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    queryset = Position.objects.prefetch_related("workers")
    paginate_by = 5


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:position-list")
        )
        return context


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:position-list")
        )
        return context


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:position-list")
        )
        return context
