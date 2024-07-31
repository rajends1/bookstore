import pytest
from django.urls import resolve, reverse

from .factories import BookFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def book():
    return BookFactory()


def test_book_list_reverse():
    """book_list should reverse to /books/."""
    assert reverse("book_list") == "/books/"


def test_book_list_resolve():
    """/books/" should resolve to book_list."""
    assert resolve("/books/").view_name == "book_list"


def test_book_add_reverse():
    """book_add should reverse to /books/add/."""
    assert reverse("book_add") == "/books/add/"


def test_book_add_resolve():
    """/books/add/" should resolve to book_add."""
    assert resolve("/books/add/").view_name == "book_add"


def test_book_detail_reverse(book):
    """book_detail should reverse to /books/uuid."""
    url = reverse("book_detail", kwargs={"pk": book.id})
    assert url == f"/books/{book.id}/"


def test_book_detail_resolve(book):
    """/books/{book.id}/ should resolve to book_detail."""
    url = f"/books/{book.id}/"
    assert resolve(url).view_name == "book_detail"
