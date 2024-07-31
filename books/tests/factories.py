import factory
import factory.fuzzy

from accounts.tests.factories import UserFactory

from ..models import Book, Review


class BookFactory(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText(length=12, prefix="The Book of ")
    author = factory.SubFactory(UserFactory)
    price = factory.fuzzy.FuzzyDecimal(low=9.95, high=99.99)
    creator = factory.SubFactory(UserFactory)

    class Meta:
        model = Book


class ReviewFactory(factory.django.DjangoModelFactory):
    book = factory.SubFactory(BookFactory)
    review = factory.fuzzy.FuzzyText(length=25, prefix="The Review of ")
    creator = factory.SubFactory(UserFactory)

    class Meta:
        model = Review
