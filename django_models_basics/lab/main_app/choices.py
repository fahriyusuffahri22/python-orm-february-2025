from django.db import models


class CityChoices(models.TextChoices):
    SOFIA = 'Sofia', 'Sofia'
    PLOVDIV = 'Plovdiv', 'Plovdiv'
    BURGAS = 'Burgas', 'Burgas'
    VARNA = 'Varna', 'Varna'
