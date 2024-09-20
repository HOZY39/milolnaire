from django.contrib import admin
from .models import Questions, FriendAnswers
# Register your models here.
admin.site.register(Questions)
admin.site.register(FriendAnswers)