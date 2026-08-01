from django import forms
from django.db import models
from django_select2.forms import Select2MultipleWidget
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Task, Tag


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=Select2MultipleWidget(
            attrs={
                "data-theme": "bootstrap-5"
            }
        ),
    )
    deadline = forms.DateField(
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "type": "date",
            }
        ),
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=Select2MultipleWidget(
            attrs={
                "data-theme": "bootstrap-5"
            }
        ),
    )

    class Meta:
        model = Task
        fields = "__all__"


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "avatar",
            "first_name",
            "last_name",
            "email",
            "position",
        )


class WorkerUpdateForm(UserChangeForm):

    password = None

    class Meta:
        model = get_user_model()
        fields = [
            "avatar",
            "first_name",
            "last_name",
            "email",
            "position",
        ]


class SearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name",
                "class": "form-control"
            }
        )
    )


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username",
                "class": "form-control"
            }
        )
    )


class TaskStatusForm(forms.Form):
    class Status(models.TextChoices):
        ALL = "all", "All"
        COMPLETED = "completed", "Completed"
        IN_PROGRESS = "in_progress", "In progress"

    status = forms.ChoiceField(
        required=False,
        label="",
        choices=Status,
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )
