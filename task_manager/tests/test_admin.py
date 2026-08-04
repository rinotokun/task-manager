from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from task_manager.models import Position


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test123"
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(name="QA")
        self.worker = get_user_model().objects.create_user(
            username="user",
            password="test123",
            position=self.position
        )

    def test_workerk_position_listed(self):
        url = reverse("admin:task_manager_worker_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.worker.position)

    def test_workerk_detail_position_avatar_listed(self):
        url = reverse(
            "admin:task_manager_worker_change",
            args=[self.worker.id]
        )
        response = self.client.get(url)
        self.assertContains(response, self.worker.position)

        admin_form = response.context["adminform"]

        self.assertIn("avatar", admin_form.form.fields)

    def test_workerk_create_position_avatar_full_name_listed(self):
        url = reverse("admin:task_manager_worker_add")
        response = self.client.get(url)

        admin_form = response.context["adminform"]

        self.assertIn("position", admin_form.form.fields)
        self.assertIn("avatar", admin_form.form.fields)
        self.assertIn("first_name", admin_form.form.fields)
        self.assertIn("last_name", admin_form.form.fields)
