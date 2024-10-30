import os

from django.core.management import BaseCommand
from dotenv import load_dotenv

from config.settings import BASE_DIR
from users.models import CustomUser


class Command(BaseCommand):
    """Создание суперпользователя"""

    def handle(self, *args, **options):
        dotenv_path = os.path.join(BASE_DIR, '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        user = CustomUser.objects.create(
            first_name='Admin',
            last_name='Root',
            phone='+70001234567',
            email=os.getenv('ADMIN_EMAIL'),
            role='admin',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password(os.getenv('ADMIN_PASSWORD'))
        user.save()
