from django.urls import path

from .views import (
    BookCreateView,
    BookDetailView,
    BookListView,
    BookUpdateView,
    ReviewCreateView,
    ReviewDeleteView,
    ReviewDetailView,
    ReviewUpdateView,
    SearchResultsListView,
)

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("add/", BookCreateView.as_view(), name="book_add"),
    path("<uuid:pk>/update/", BookUpdateView.as_view(), name="book_update"),
    path("<uuid:pk>/", BookDetailView.as_view(), name="book_detail"),
    path(
        "<uuid:book_id>/review/add/",
        ReviewCreateView.as_view(),
        name="review_create",
    ),
    path(
        "<uuid:book_id>/review/<int:pk>/",
        ReviewDetailView.as_view(),
        name="review_detail",
    ),
    path(
        "<uuid:book_id>/review/<int:pk>/update/",
        ReviewUpdateView.as_view(),
        name="review_update",
    ),
    path(
        "<uuid:book_id>/review/<int:pk>/delete/",
        ReviewDeleteView.as_view(),
        name="review_delete",
    ),
    path("search/", SearchResultsListView.as_view(), name="search_results"),
]
