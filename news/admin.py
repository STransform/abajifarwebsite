from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import NewsArticle, NewsCategory


@admin.register(NewsArticle)
class NewsArticleAdmin(TranslationAdmin):
    list_display = ("title", "news_category", "created_by", "minutes_read", "created_at")
    list_filter = ("news_category", "created_at")
    search_fields = ("title", "content", "created_by__first_name", "created_by__last_name")


@admin.register(NewsCategory)
class NewsCategoryAdmin(TranslationAdmin):
    list_display = ("name",)
    search_fields = ("name",)
