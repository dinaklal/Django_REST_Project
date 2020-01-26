from django.contrib import admin

from test_api import models


admin.site.register(models.UserProfile)
admin.site.register(models.Review)
