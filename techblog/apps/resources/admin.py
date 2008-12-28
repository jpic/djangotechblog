from django.contrib import admin

import models


class ImageUploadAdmin(admin.ModelAdmin):
    fields = ( 'owner',
               'name',
              'image',
              'description'
              )
    list_display = ('name', 'html_image')


admin.site.register(models.ImageUpload, ImageUploadAdmin)
