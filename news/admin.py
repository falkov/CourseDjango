from django.contrib import admin

from .models import Category, Tag, Post, Comment

admin.site.site_header = 'Привет, falkov!'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'amount_for_pagination', 'template',)
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    # непонятно, как вернуть из модели Category значение поля 'amount_for_pagination'
    # или как вызвать функцию модели pagination_amount(), которая возвращает это
    # list_per_page = int(Category.pagination_amount)
    list_per_page = 20  # пока так будет



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class CommentInline(admin.TabularInline):
    """Комменты будут редактироваться на странице Постов"""
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'subtitle', 'user', 'slug', 'text_short', 'created_short', 'edited_short', 'published_short',
        'do_publish', 'show_for_all',
    )
    list_display_links = ('title',)
    list_filter = ('created', 'category', 'tags',)
    list_editable = ('do_publish', 'show_for_all',)
    search_fields = ('title',)

    readonly_fields = ('created',)
    prepopulated_fields = {'slug': ('title',)}

    inlines = [CommentInline]
