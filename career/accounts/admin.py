from django.contrib import admin
from .models import User, UserProfile, TrainerProfile
# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(TrainerProfile)
