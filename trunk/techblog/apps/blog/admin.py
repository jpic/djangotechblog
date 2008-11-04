#!/usr/bin/env python
from django.contrib import admin

import models


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(models.Blog, BlogAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'post_time', 'get_admin_abbrev']
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = 'post_time'

admin.site.register(models.Post, PostAdmin)