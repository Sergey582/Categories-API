from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create admin user for docker"

    def handle(self, *args, **kwargs):
        username = 'admin'
        email = 'admin@admin-soft.com'
        password = 'admin'
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            is_active=True,
                                            is_staff=True,
                                            is_superuser=True)
