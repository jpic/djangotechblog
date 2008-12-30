from django.contrib import admin

import models


class PageBaseAdmin(admin.ModelAdmin):
    fields = (  'name',
                'content_markup_type',
                'content',
                'template' )
    radio_fields={'content_markup_type':admin.HORIZONTAL}
    list_display = ['__unicode__', 'template']

admin.site.register(models.PageBase, PageBaseAdmin)


class PageAdmin(admin.ModelAdmin):
    fields = ('base',
              'parent',
              'path',
              'title',
              'content_markup_type',
              'content',
              )

    radio_fields={'content_markup_type':admin.HORIZONTAL}
    list_display = ['__unicode__', 'path']
    search_fields=('title', )

admin.site.register(models.Page, PageAdmin)