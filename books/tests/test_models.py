import pytest

pytestmark = pytest.mark.django_db


def test_book__str__(book):
    assert book.__str__() == book.title
    assert str(book) == book.title


def test_book_get_absolute_url(book):
    url = book.get_absolute_url()
    assert url == f"/books/{book.id}/"


def test_review__str__(review):
    assert review.__str__() == review.review
    assert str(review) == review.review


def test_review_get_absolute_url(review):
    url = review.get_absolute_url()
    assert url == f'{"/books/"}'
