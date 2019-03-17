from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from mptt.forms import TreeNodeChoiceField

from .models import Category, Tag, Post, Comment

admin.site.site_header = 'Привет, falkov!'


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('id', 'name', 'slug', 'amount_for_pagination', 'short_post_template', 'detail_post_template',)
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    mptt_indent_field = 'name'
    mptt_level_indent = 30

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
        'id', 'title', 'subtitle', 'user', 'category','slug', 'text_short', 'created_date_short', 'edited_date_short', 'published_date_short',
        'do_publish', 'show_for_all',
    )
    list_display_links = ('title',)
    list_filter = ('created_date', 'category', 'tags',)
    list_editable = ('do_publish', 'show_for_all',)
    search_fields = ('title',)

    readonly_fields = ('created_date',)
    prepopulated_fields = {'slug': ('title',)}

    inlines = [CommentInline]
