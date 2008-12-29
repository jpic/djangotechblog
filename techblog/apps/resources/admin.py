from django.contrib import admin

import models


class ImageUploadAdmin(admin.ModelAdmin):
    fields = ( 'owner',
               'name',
              'image',
              'description'
              )
    list_display = ('name', 'html_image')
    search_fields = ['name', 'description']


admin.site.register(models.ImageUpload, ImageUploadAdmin)
