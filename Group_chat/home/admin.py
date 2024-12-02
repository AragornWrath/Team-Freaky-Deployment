from django.contrib import admin
from .models import TripItem

admin.site.register(TripItem)
import home.models
# Register your models here.

admin.site.register(home.models.userModel)