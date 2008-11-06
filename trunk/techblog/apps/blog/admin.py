#!/usr/bin/env python
from django.contrib import admin

import models



class BlogAdmin(admin.ModelAdmin):
    fields = ('title',
              'slug',
              'markup_type',
              'markup_raw',
              'html',
              'summary_html')
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(models.Blog, BlogAdmin)


class PostAdmin(admin.ModelAdmin):
    fields = ('blog',
              'title',
              'slug',
              'published',
              'display_time',
              'tags',
              'markup_type',
              'markup_raw',
              'html',
              'summary_html',
              'data')
    list_display = ['__unicode__', 'display_time', 'get_admin_abbrev']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'display_time'

admin.site.register(models.Post, PostAdmin)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__unicode__', 'count')

admin.site.register(models.Tag, TagAdmin)