#!/usr/bin/env python
from django.contrib import admin

import models


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(models.Blog, BlogAdmin)


class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'published', 'display_time', 'markup_type', 'markup_raw')
    list_display = ['__unicode__', 'display_time', 'get_admin_abbrev']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'display_time'

admin.site.register(models.Post, PostAdmin)