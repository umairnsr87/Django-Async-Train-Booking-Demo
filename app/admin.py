from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.LoginSession)
admin.site.register(models.UserModel)
admin.site.register(models.Booking)
admin.site.register(models.Train)
