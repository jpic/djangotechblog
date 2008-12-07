#!/usr/bin/env python
from django.contrib import admin

import models



class BlogAdmin(admin.ModelAdmin):
    fields = ('title',
              'slug',
              'tagline',
              'description_markup_type',
              'description',
              'description_html',
              )
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['__unicode__', 'tagline']

admin.site.register(models.Blog, BlogAdmin)


class PostAdmin(admin.ModelAdmin):
    fields = ('blog',
              'title',
              'slug',
              'published',
              'display_time',
              'tags_text',
              'content',
              'content_html',
              'content_summary_html')
    list_display = ['__unicode__', 'display_time', 'get_admin_abbrev']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'display_time'

admin.site.register(models.Post, PostAdmin)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug', 'count')

admin.site.register(models.Tag, TagAdmin)