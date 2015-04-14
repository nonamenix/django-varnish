from django.contrib import admin
from blog.models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'datetime', 'is_important')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)