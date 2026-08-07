from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Count, Case, Value, When
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

from task_manager.models import Task, TaskType, Position, Tag
from task_manager.forms import (
    TaskForm,
    WorkerCreationForm,
    WorkerUpdateForm,
    SearchForm,
    WorkerSearchForm,
    TaskStatusForm,
    TaskCreateForm,
)


@login_required
def index(request):
    date_today = timezone.localdate()
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
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = SearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.select_related(
            "task_type"
        ).prefetch_related("assignees", "tags")
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_queryset(self):
        queryset = Task.objects.select_related(
            "task_type"
        ).prefetch_related("assignees", "tags")
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
    form_class = TaskCreateForm
    success_url = reverse_lazy("task_manager:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_url"] = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:task-list")
        )
        return context


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        if self.request.GET.get("next"):
            return self.request.GET.get("next")
        return reverse(
            "task_manager:task-detail",
            kwargs={"pk": self.object.id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_url"] = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:task-list")
        )
        return context


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
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = SearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = TaskType.objects.prefetch_related("tasks")
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


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
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = SearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Position.objects.prefetch_related("workers")
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


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


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 8

    def get_queryset(self):
        queryset = get_user_model().objects.select_related(
            "position"
        ).prefetch_related("tasks")
        username = self.request.GET.get("username")
        if username:
            return queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()

    def get_queryset(self):
        queryset = get_user_model().objects.select_related(
            "position"
        ).prefetch_related("tasks")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        back_url = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:worker-list")
        )
        status = self.request.GET.get("status")
        context["status_select"] = TaskStatusForm(
            initial={"status": status}
        )
        tasks = self.object.tasks.select_related(
            "task_type"
        ).prefetch_related("assignees", "tags").order_by("deadline")
        if status == "completed":
            tasks = tasks.filter(is_completed=True)
        elif status == "in_progress":
            tasks = tasks.filter(is_completed=False)
        assigned_tasks = self.object.tasks.count()
        completed_tasks = self.object.tasks.filter(
            is_completed=True
        ).count()
        tasks_in_progress = assigned_tasks - completed_tasks
        paginator = Paginator(tasks, 3)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        is_paginated = paginator.num_pages > 1
        context |= {
            "back_url": back_url,
            "assigned_tasks": assigned_tasks,
            "completed_tasks": completed_tasks,
            "tasks_in_progress": tasks_in_progress,
            "is_paginated": is_paginated,
            "paginator": paginator,
            "page_number": page_number,
            "page_obj": page_obj,
        }
        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task_manager:worker-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:worker-list")
        )
        return context


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = WorkerUpdateForm

    def get_success_url(self):
        if self.request.GET.get("next"):
            return self.request.GET.get("next")
        return reverse(
            "task_manager:worker-detail",
            kwargs={"pk": self.object.id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:worker-list")
        )
        return context


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("task_manager:worker-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:worker-list")
        )
        return context


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = SearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Tag.objects.prefetch_related("tasks")
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tag-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:tag-list")
        )
        return context


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tag-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:tag-list")
        )
        return context


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("task_manager:tag-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.request.GET.get(
            "next",
            reverse_lazy("task_manager:tag-list")
        )
        return context
