from django.db import models

# Create your models here.
from .models import * # noqa

from .models.permission import Permission  # <-- Assure-toi qu'il est là
from .models.group import Group  # <-- Assure-toi qu'il est là
from .models.page import Page  # <-- Assure-toi qu'il est là
from .models.module import Module  # <-- Assure-toi qu'il est là

# ... (Group et Permission n'y sont plus, c'est bien)

__all__ = [
    'Page',
    'Module',
    'Permission',
    'Group',
]