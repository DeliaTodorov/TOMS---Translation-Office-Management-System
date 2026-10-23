from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # TextChoices = o listă fixă de valori permise (ca un enum)
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrator"
        MANAGER = "manager", "Manager"
        TRANSLATOR = "translator", "Traducător"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MANAGER,
    )
    phone = models.CharField("Telefon", max_length=20, blank=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
