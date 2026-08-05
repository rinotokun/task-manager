from datetime import timedelta

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from task_manager.models import (
    Task,
    TaskType,
    Tag,
    Position
)


URLS = {
    "MAIN_PAGE_URL": reverse("task_manager:index"),
    "TASK_LIST_URL": reverse("task_manager:task-list"),
    "TASK_CREATE_URL": reverse("task_manager:task-create"),
    "TASK_DETAIL_URL": reverse("task_manager:task-detail", args=[1]),
    "TASK_UPDATE_URL": reverse("task_manager:task-update", args=[1]),
    "TASK_DELETE_URL": reverse("task_manager:task-delete", args=[1]),
    "POSITION_LIST_URL": reverse("task_manager:position-list"),
    "POSITION_CREATE_URL": reverse("task_manager:position-create"),
    "POSITION_UPDATE_URL": reverse("task_manager:position-update", args=[1]),
    "POSITION_DELETE_URL": reverse("task_manager:position-delete", args=[1]),
    "TAG_LIST_URL": reverse("task_manager:tag-list"),
    "TAG_CREATE_URL": reverse("task_manager:tag-create"),
    "TAG_UPDATE_URL": reverse("task_manager:tag-update", args=[1]),
    "TAG_DELETE_URL": reverse("task_manager:tag-delete", args=[1]),
    "TASK_TYPE_LIST_URL": reverse("task_manager:tasktype-list"),
    "TASK_TYPE_CREATE_URL": reverse("task_manager:tasktype-create"),
    "TASK_TYPE_UPDATE_URL": reverse(
        "task_manager:tasktype-update",
        args=[1]
    ),
    "TASK_TYPE_DELETE_URL": reverse(
        "task_manager:tasktype-delete",
        args=[1]
    ),
    "WORKER_LIST_URL": reverse("task_manager:worker-list"),
    "WORKER_CREATE_URL": reverse("task_manager:worker-create"),
    "WORKER_DETAIL_URL": reverse("task_manager:worker-detail", args=[1]),
    "WORKER_UPDATE_URL": reverse("task_manager:worker-update", args=[1]),
    "WORKER_DELETE_URL": reverse("task_manager:worker-delete", args=[1]),
}


class LoginRequiredTest(TestCase):

    def setUp(self):

        self.client = Client()

        self.date_today = timezone.localdate()
        self.worker = get_user_model().objects.create_user(
            username="user",
            password="test123"
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.tag = Tag.objects.create(name="bugs")
        self.position = Position.objects.create(name="QA")
        self.task = Task.objects.create(
            name="Test task",
            description="Some description",
            deadline=self.date_today,
            priority=Task.Priority.HIGH
        )

    def test_login_required_pages(self):

        for url in URLS.keys():
            with self.subTest(url=url):
                response = self.client.get(URLS[url])
                expected_url = reverse("login") + "?next=" + URLS[url]

                self.assertRedirects(response, expected_url, status_code=302)


class SearchFormTest(TestCase):

    def setUp(self):
        self.tag1 = Tag.objects.create(name="Bug")
        self.tag2 = Tag.objects.create(name="fix")
        self.tag3 = Tag.objects.create(name="QA")
        self.tag4 = Tag.objects.create(name="Test")

        self.user1 = get_user_model().objects.create_user(
            username="user1",
            password="test123"
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2",
            password="test123"
        )
        self.user3 = get_user_model().objects.create_user(
            username="user3",
            password="test123"
        )

        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="test123"
        )
        self.client.force_login(self.admin)

    def test_empty_search_returns_all_tags(self):
        response = self.client.get(URLS["TAG_LIST_URL"], {"name": ""})

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["tag_list"],
            Tag.objects.all(),
        )

    def test_search_filters_by_name(self):
        response = self.client.get(URLS["TAG_LIST_URL"], {"name": "qa"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["tag_list"]), 1)
        self.assertContains(response, self.tag3.name)

    def test_empty_search_returns_all_workers(self):
        response = self.client.get(URLS["WORKER_LIST_URL"], {"username": ""})

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["worker_list"],
            get_user_model().objects.all(),
        )

    def test_search_filters_by_username(self):
        response = self.client.get(
            URLS["WORKER_LIST_URL"],
            {"username": "er2"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["worker_list"]), 1)
        self.assertContains(response, self.user2.username)


class WorkerDetailTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="test123"
        )
        self.client.force_login(self.admin)

        self.date_today = timezone.localdate()
        self.task1 = Task.objects.create(
            name="Test task1",
            description="Some description",
            deadline=self.date_today,
            is_completed=False,
            priority=Task.Priority.HIGH
        )
        self.task2 = Task.objects.create(
            name="Test task2",
            description="Some description",
            deadline=self.date_today,
            is_completed=False,
            priority=Task.Priority.HIGH
        )
        self.task3 = Task.objects.create(
            name="Test task3",
            description="Some description",
            deadline=self.date_today,
            is_completed=False,
            priority=Task.Priority.HIGH
        )
        self.task4 = Task.objects.create(
            name="Test task4",
            description="Some description",
            deadline=self.date_today,
            is_completed=True,
            priority=Task.Priority.HIGH
        )
        self.task5 = Task.objects.create(
            name="Test task5",
            description="Some description",
            deadline=self.date_today,
            is_completed=True,
            priority=Task.Priority.HIGH
        )
        self.task6 = Task.objects.create(
            name="Not assigned task",
            description="Some description",
            deadline=self.date_today,
            is_completed=True,
            priority=Task.Priority.HIGH
        )
        self.task1.assignees.add(self.admin)
        self.task2.assignees.add(self.admin)
        self.task3.assignees.add(self.admin)
        self.task4.assignees.add(self.admin)
        self.task5.assignees.add(self.admin)

    def test_filter_when_selected_all(self):
        url = reverse("task_manager:worker-detail", args=[self.admin.id])

        response = self.client.get(url, {"status": "all"})
        expected_queryset = get_user_model().objects.get(
            id=self.admin.id
        ).tasks.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["paginator"].object_list), 5)
        self.assertQuerySetEqual(
            response.context["paginator"].object_list,
            expected_queryset,
        )

    def test_filter_when_selected_completed(self):
        url = reverse("task_manager:worker-detail", args=[self.admin.id])

        response = self.client.get(url, {"status": "completed"})
        expected_queryset = get_user_model().objects.get(
            id=self.admin.id
        ).tasks.filter(is_completed=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["paginator"].object_list), 2)
        self.assertQuerySetEqual(
            response.context["paginator"].object_list,
            expected_queryset,
        )

    def test_filter_when_selected_in_progress(self):
        url = reverse("task_manager:worker-detail", args=[self.admin.id])

        response = self.client.get(url, {"status": "in_progress"})
        expected_queryset = get_user_model().objects.get(
            id=self.admin.id
        ).tasks.filter(is_completed=False)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["paginator"].object_list), 3)
        self.assertQuerySetEqual(
            response.context["paginator"].object_list,
            expected_queryset,
        )

    def test_worker_detail_counters(self):
        url = reverse("task_manager:worker-detail", args=[self.admin.id])

        response = self.client.get(url)

        self.assertEqual(response.context["assigned_tasks"], 5)
        self.assertEqual(response.context["completed_tasks"], 2)
        self.assertEqual(response.context["tasks_in_progress"], 3)


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="test123"
        )
        self.client.force_login(self.admin)

        self.date_today = timezone.localdate()
        self.date_tomorrow = timezone.localdate() + timedelta(days=1)
        self.date_yesterday = timezone.localdate() - timedelta(days=1)
        self.task1 = Task.objects.create(
            name="Test task1",
            description="Some description",
            deadline=self.date_today,
            is_completed=False,
            priority=Task.Priority.URGENT
        )
        self.task2 = Task.objects.create(
            name="Test task2",
            description="Some description",
            deadline=self.date_tomorrow,
            is_completed=False,
            priority=Task.Priority.URGENT
        )
        self.task3 = Task.objects.create(
            name="Test task3",
            description="Some description",
            deadline=self.date_tomorrow,
            is_completed=False,
            priority=Task.Priority.HIGH
        )
        self.task4 = Task.objects.create(
            name="Test task4",
            description="Some description",
            deadline=self.date_today,
            is_completed=True,
            priority=Task.Priority.MEDIUM
        )
        self.task5 = Task.objects.create(
            name="Test task5",
            description="Some description",
            deadline=self.date_today,
            is_completed=True,
            priority=Task.Priority.LOW
        )
        self.task6 = Task.objects.create(
            name="Not assigned task",
            description="Some description",
            deadline=self.date_yesterday,
            is_completed=False,
            priority=Task.Priority.HIGH
        )

    def test_task_counts(self):
        response = self.client.get(URLS["MAIN_PAGE_URL"])

        self.assertEqual(response.context["num_tasks"], 6)
        self.assertEqual(response.context["completed"], 2)
        self.assertEqual(response.context["in_progress"], 4)
        self.assertEqual(response.context["overdue"], 1)

    def test_upcoming_deadlines(self):
        response = self.client.get(URLS["MAIN_PAGE_URL"])
        expected_result = Task.objects.filter(
            is_completed=False
        ).order_by("deadline")[:5]

        self.assertQuerySetEqual(
            response.context["upcoming_deadlines"],
            expected_result
        )

    def test_tasks_by_priority(self):
        response = self.client.get(URLS["MAIN_PAGE_URL"])
        result = {
            task["priority"]: task["count"]
            for task in response.context["tasks_by_priority"]
        }

        expected_result = {
            "Urgent": 2,
            "High": 2,
            "Medium": 1,
            "Low": 1,
        }

        self.assertDictEqual(result, expected_result)
