from django.contrib import admin
from .models import Event

class AdminEvent(admin.ModelAdmin):
    list_display = ['title','description','start_time','end_time','User']

admin.site.register(Event,AdminEvent)