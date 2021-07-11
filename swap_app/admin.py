from django.contrib import admin

# Register your models here.

from .models import User, Recipe, Suggestion, Image

admin.site.register(User)
admin.site.register(Recipe)
admin.site.register(Suggestion)
admin.site.register(Image)