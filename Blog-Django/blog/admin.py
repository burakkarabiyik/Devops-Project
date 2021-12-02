from django.contrib import admin
from django.db import models
from blog.models import Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "publishing_date", 'slug','status']
    list_display_links = ["slug","title"]
    list_filter = ["publishing_date"]
    search_fields = ["title","user", "content"]
    # list_editable = ["title"]

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)
