from django.contrib import admin

from .models import Book, Review


class ReviewInline(admin.TabularInline):
    model = Review


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "description",
        "price",
        "publisher",
        "pubdate",
    ]
    search_fields = ["title", "author"]
    ordering = ["title", "author"]
    inlines = [
        ReviewInline,
    ]


admin.site.register(Review)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["review", "date", "creator"]
    search_fields = ["creator", "review"]
