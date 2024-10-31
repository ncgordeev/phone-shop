import os

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

NULLABLE = {"null": True, "blank": True}


def validate_image(image):
    valid_extensions = ['jpg', 'jpeg', 'png', 'webp']
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(_(f'Unsupported file type {ext}. Supported types: {", ".join(valid_extensions)}'))
