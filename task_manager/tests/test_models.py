from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from task_manager.models import (
    TaskType,
    Tag,
    Task,
    Position,
)


class ModelTest(TestCase):

    def setUp(self):
        self.date_today = timezone.now().date()
        self.worker1 = get_user_model().objects.create_user(
            username="user1",
            password="test123"
        )
        self.worker2 = get_user_model().objects.create_user(
            username="user2",
            password="test123",
            first_name="First",
            last_name="Last"
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.tag = Tag.objects.create(name="bugs")
        self.position = Position.objects.create(name="QA")
        self.task = Task.objects.create(
            name="Test task",
            description="Some description",
            deadline=self.date_today,
            is_completed=False,
            task_type=self.task_type
        )
        self.task.assignees.add(self.worker1)
        self.task.tags.add(self.tag)

    def test_task_type_str(self):
        self.assertEqual(
            str(self.task_type),
            f"{self.task_type.name}"
        )

    def test_position_str(self):
        self.assertEqual(
            str(self.position),
            f"{self.position.name}"
        )

    def test_tag_str(self):
        self.assertEqual(
            str(self.tag),
            f"{self.tag.name}"
        )

    def test_worker_without_first_name_last_name_str(self):
        self.assertEqual(
            str(self.worker1),
            f"{self.worker1.username} ( )"
        )

    def test_worker_with_first_name_last_name_str(self):
        self.assertEqual(
            str(self.worker2),
            f"{self.worker2.username} (First Last)"
        )

    def test_task_str(self):
        self.assertEqual(
            str(self.task),
            f"{self.task.name} {self.task.deadline.strftime('%d.%m.%Y')}"
        )

    def test_default_task_priority(self):
        self.assertEqual(
            self.task.priority,
            Task.Priority.LOW
        )


class TaskPriorityColorTest(TestCase):

    def setUp(self):
        data_task = {
            "name": "Test task",
            "description": "Some description",
            "deadline": timezone.now().date(),
            "is_completed": False,
        }
        self.tasks_dict = {
            "low": Task.objects.create(
                **data_task,
                priority=Task.Priority.LOW
            ),
            "high": Task.objects.create(
                **data_task,
                priority=Task.Priority.HIGH
            ),
            "medium": Task.objects.create(
                **data_task,
                priority=Task.Priority.MEDIUM
            ),
            "urgent": Task.objects.create(
                **data_task,
                priority=Task.Priority.URGENT
            ),
            "fallback": Task.objects.create(
                **data_task,
                priority="some_priority"
            ),
        }

    def test_task_priority_color_low(self):
        self.assertEqual(
            self.tasks_dict["low"].priority_color(),
            "secondary"
        )

    def test_task_priority_color_high(self):
        self.assertEqual(
            self.tasks_dict["high"].priority_color(),
            "warning"
        )

    def test_task_priority_color_medium(self):
        self.assertEqual(
            self.tasks_dict["medium"].priority_color(),
            "info"
        )

    def test_task_priority_color_urgent(self):
        self.assertEqual(
            self.tasks_dict["urgent"].priority_color(),
            "danger"
        )

    def test_task_priority_color_fallback(self):
        self.assertEqual(
            self.tasks_dict["fallback"].priority_color(),
            "secondary"
        )
