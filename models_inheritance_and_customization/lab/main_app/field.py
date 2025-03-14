from django.db import models
from main_app.choices import AvailabilityChoices


class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = AvailabilityChoices.choices
        kwargs['default'] = True

        super().__init__(*args, **kwargs)
