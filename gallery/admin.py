from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')

# from django.contrib import admin
# from .models import Image
#
# # Register your models here.
#
# admin.site.register(Image)