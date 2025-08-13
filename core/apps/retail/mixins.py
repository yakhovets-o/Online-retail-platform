from django.db import models
from django.utils import timezone


class CreatedUpdatedMixin(models.Model):
    """Mixins add created and updated timestamp fields in model"""

    created = models.DateTimeField(
        default=timezone.now, editable=False, verbose_name="Дата создания"
    )
    updated = models.DateTimeField(
        auto_now=True, editable=False, verbose_name="Дата обновления"
    )

    class Meta:
        abstract = True
