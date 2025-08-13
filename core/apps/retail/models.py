from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from core.apps.retail.choices import SupplierChoices
from core.apps.retail.mixins import CreatedUpdatedMixin
from core.apps.users.models import User


class Supplier(CreatedUpdatedMixin, models.Model):
    """Retail network Supplier model"""

    title = models.CharField(max_length=50, verbose_name="Название")
    type_supplier = models.IntegerField(
        choices=SupplierChoices.choices, verbose_name="Тип Сети"
    )
    debt = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name="Задолженность",
    )

    contact = models.OneToOneField(
        "Contact", on_delete=models.CASCADE, verbose_name="Контакт"
    )
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Поставщик",
    )  # Supplier
    employees = models.ManyToManyField(User, verbose_name="Сотрудник")
    products = models.ManyToManyField(
        "Product", related_name="network_nodes", verbose_name="Доступные продукты"
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
        ordering = ["-created", "-debt", "title"]

    def clean(self):
        """Validate supplier hierarchy."""

        if self.type_supplier == SupplierChoices.FACTORY and self.supplier:
            raise ValidationError("Завод не может иметь поставщика!")

    @property
    def level(self) -> int:
        if self.type_supplier == SupplierChoices.FACTORY:
            return 0

        level = 0
        current = self
        while current.supplier:
            level += 1
            current = current.supplier
        return level


class Contact(models.Model):
    """Contact model supplier"""

    email = models.EmailField(
        max_length=100, unique=True, verbose_name="Электронная почта"
    )
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=50, verbose_name="Номер дома")

    def __str__(self):
        return f"{self.country},  {self.city}, {self.street}, {self.house_number}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ["country"]


class Product(models.Model):
    """Product model supplier"""

    name = models.CharField(max_length=25, verbose_name="Название")
    model = models.CharField(max_length=100, verbose_name="Модель")

    date_product_release = models.DateTimeField(
        default=timezone.now, verbose_name="Дата выхода"
    )

    def __str__(self):
        return f"{self.name},  {self.model}, {self.date_product_release}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["-date_product_release"]
