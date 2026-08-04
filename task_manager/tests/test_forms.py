from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from task_manager.models import Task
from task_manager.forms import TaskCreateForm, TaskForm


class ValidDateTaskForm(TestCase):

    @staticmethod
    def create_form(date):
        return TaskCreateForm(
            data={
                "name": "Test name",
                "description": "Test description",
                "priority": Task.Priority.LOW,
                "deadline": date
            }
        )

    def test_validation_deadline_when_date_is_yesterday(self):
        yesterday = timezone.localdate() - timedelta(days=1)
        form = self.create_form(yesterday)
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)

    def test_validation_deadline_when_date_is_current_day(self):
        current_day = timezone.localdate()
        self.assertTrue(self.create_form(current_day).is_valid())

    def test_validation_deadline_when_date_is_tomorrow(self):
        tomorrow = timezone.localdate() + timedelta(days=1)
        self.assertTrue(self.create_form(tomorrow).is_valid())

    def test_can_update_task_when_date_is_yesterday(self):
        yesterday = timezone.localdate() - timedelta(days=1)
        test_form = TaskForm(
            data={
                "name": "Test name",
                "description": "Test description",
                "priority": Task.Priority.LOW,
                "deadline": yesterday
            }
        )
        self.assertTrue(test_form.is_valid())
