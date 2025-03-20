import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class NameValidator:
    def __init__(self, message):
        self.message = message

    def __call__(self, value):
        if not re.fullmatch(r'[A-Za-z\s]*', value):
            raise ValidationError('Name can only contain letters and spaces')


@deconstructible
class PhoneNumberValidator:
    def __init__(self, message):
        self.message = message

    def __call__(self, value):
        if not re.fullmatch(r'\+359\d{9}', value):
            raise ValidationError("Phone number must start with '+359' followed by 9 digits")
