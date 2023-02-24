import os

if os.environ.get("DJANGO_ENV") == "PRODUCTION":
    from .settings_prod import *
else:
    from .settings_dev import *
