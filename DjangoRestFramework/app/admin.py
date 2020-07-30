from django.contrib import admin
from .models import Data

# Register your models here.
class DataAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']
    list_per_page = 10
    search_fields = ('text', 'id')





admin.site.register(Data, DataAdmin)

