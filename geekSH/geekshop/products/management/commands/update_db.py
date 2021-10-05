from django.core.management.base import BaseCommand
from users.models import NormalUser
from users.models import UserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = NormalUser.objects.all()
        for user in users:
            users_profile = UserProfile.objects.create(user=user)
            users_profile.save()