from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')  # 보여줄 항목
    list_filter = ('status', 'created', 'publish', 'author')  # 필터
    search_fields = ('title', 'body')  # 검색창
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']  # 정렬


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
