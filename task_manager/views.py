from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Task


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
