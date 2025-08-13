from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Model of the user (employee)."""

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
