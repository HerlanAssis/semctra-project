from django.contrib import admin
from .models import Schedule, Event, Interval
# Register your models here.

admin.site.register(Schedule)
admin.site.register(Event)
admin.site.register(Interval)
