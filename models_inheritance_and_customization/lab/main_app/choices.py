from django.db import models


class AvailabilityChoices(models.IntegerChoices):
    AVAILABLE = 1, 'Available'
    NOT_AVAILABLE = 0, 'Not Available'
