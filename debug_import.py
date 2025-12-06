import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

try:
    from apps.profilmanagement.api.controllers.user_controller import UserController
    print("SUCCESS: UserController imported successfully.")
except Exception as e:
    print(f"ERROR: Failed to import UserController. Reason: {e}")
    import traceback
    traceback.print_exc()
