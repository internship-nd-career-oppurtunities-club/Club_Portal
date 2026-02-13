from django.contrib import admin

from .models import User, Activities, Rounds, Resources
# Register your models here.
admin.site.register(User)
admin.site.register(Activities)
admin.site.register(Rounds)
admin.site.register(Resources)

