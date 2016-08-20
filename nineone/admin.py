from django.contrib import admin
from models import NineoneVideo

# Register your models here.

class NineoneVideoAdmin(admin.ModelAdmin):
    pass
admin.site.register(NineoneVideo, NineoneVideoAdmin)

