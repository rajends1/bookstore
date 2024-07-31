from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Book, Review


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = [
        "title",
        "author",
        "description",
        "price",
        "publisher",
        "pubdate",
        "cover",
    ]

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class BookDetailView(DetailView):
    model = Book
    context_object_name = "book"
    login_url = "account_login"


class BookListView(ListView):
    model = Book
    context_object_name = "book_list"
    login_url = "account_login"

    paginate_by = 5


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = [
        "title",
        "author",
        "description",
        "price",
        "publisher",
        "pubdate",
        "cover",
    ]
    action = "Update"


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ["book", "review"]

    def get_initial(self):
        initial_data = super(ReviewCreateView, self).get_initial()
        book = Book.objects.get(id=self.kwargs["book_id"])
        initial_data["book"] = book
        return initial_data

    def get_context_data(self):
        context = super(ReviewCreateView, self).get_context_data()
        book = Book.objects.get(id=self.kwargs["book_id"])
        context["book"] = book
        context["title"] = "Add a new review"
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("book_detail", args=[self.object.book_id])


class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
    context_object_name = "review"


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ["book", "review"]
    action = "Update"

    def get_success_url(self):
        return reverse("book_detail", args=[self.object.book_id])


class ReviewDeleteView(DeleteView):
    model = Review

    def get_success_url(self):
        return reverse("book_detail", args=[self.object.book_id])


class SearchResultsListView(ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "books/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
