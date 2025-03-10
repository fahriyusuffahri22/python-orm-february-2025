from django.db import models


class StatusChoices(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    COMPLETED = 'Completed', 'Completed'
    CANCELLED = 'Cancelled', 'Cancelled'
