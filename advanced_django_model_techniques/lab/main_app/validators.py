from django.core.exceptions import ValidationError


def validate_menu_categories(value):
    if not all(category in value for category in ('Appetizers', 'Main Course', 'Desserts')):
        raise ValidationError('The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')
