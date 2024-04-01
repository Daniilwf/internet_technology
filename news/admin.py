from django.contrib import admin
from .models import Profile, Article, Category, Event


# Register your models here.
@admin.register(Profile, Article, Category, Event)
class Admin(admin.ModelAdmin):
    pass
