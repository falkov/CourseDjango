from django.contrib import admin

from .models import Category, Tag, Post, Comment

admin.site.site_header = 'Привет, falkov!'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class CommentInline(admin.TabularInline):
    """Комменты будут редактироваться на странице Постов"""
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'text_short', 'created',)  # можно указывать поля и функции
    list_display_links = ('title',)
    search_fields = ('title',)  # только текстовые поля (типа CharField или TextField)
    list_filter = ('created', 'category', 'tags',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CommentInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)

# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'moderation', 'post_title_short', 'text_short', 'created',)

# admin.site.register(Comment)  # Комменты будут редактироваться на странице Постов
