#!/usr/bin/env python
from django.contrib import admin

import models

class BlogAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Blog, BlogAdmin)


class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Post, PostAdmin)