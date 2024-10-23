import random
import string
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from delivery.models import Task, TaskStatusEnum


class Command(BaseCommand):
    help = 'Seed random 10 tasks'

    def handle(self, *args, **options):
        for _ in range(10):
            Task.objects.create(
                title=''.join(random.choices(string.ascii_lowercase, k=10)),
                description=''.join(random.choices(string.ascii_lowercase, k=20)),
                status=random.choice(TaskStatusEnum.values),
                due_date=datetime.now() + timedelta(days=random.randint(1, 10))
            )

        self.stdout.write(self.style.SUCCESS('10 tasks created successfully'))