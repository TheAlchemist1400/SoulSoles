from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username = "adminfix").exists():
        User.objects.create_superuser(
            username = "adminfix",
            email = "emailfix@example.com",
            password = "StrongPassword123!")
    
    print("Superuser created: adminfix / StrongPassword123!")
