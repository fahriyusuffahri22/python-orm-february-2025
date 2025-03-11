from django.db import models


class RoomTypeChoices(models.TextChoices):
    STANDARD = 'Standard', 'Standard'
    DELUXE = 'Deluxe', 'Deluxe'
    SUITE = 'Suite', 'Suite'


class ClassNameChoices(models.TextChoices):
    MAGE = 'Mage', 'Mage'
    WARRIOR = 'Warrior', 'Warrior'
    ASSASSIN = 'Assassin', 'Assassin'
    SCOUT = 'Scout', 'Scout'
