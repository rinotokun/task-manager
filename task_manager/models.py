from django.db import models
from django.contrib.auth.models import AbstractUser


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        related_name="workers"
    )

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "Urgent"
        HIGH = "High"
        MEDIUM = "Medium"
        LOW = "Low"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority,
        default=Priority.LOW
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.SET_NULL,
        related_name="tasks",
        null=True,
        blank=True
    )
    assignees = models.ManyToManyField(
        Worker,
        related_name="tasks",
        blank=True
    )

    class Meta:
        ordering = ["-deadline"]

    def __str__(self):
        return f"{self.name} {self.deadline.strftime('%d.%m.%Y')}"
