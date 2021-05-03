from django.contrib import admin
from .models import SampleStatus, SampleCollection, Profile
# Register your models here.

admin.site.register(SampleCollection)
admin.site.register(SampleStatus)
admin.site.register(Profile)