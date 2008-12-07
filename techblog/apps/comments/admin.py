#!/usr/bin/env python
from django.contrib import admin

import models



class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Comment, CommentAdmin)
