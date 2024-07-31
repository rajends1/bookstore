import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    publisher = models.CharField(max_length=50, blank=True)
    pubdate = models.DateField(null=True, blank=True, help_text="Date of Publication")
    description = models.TextField(
        max_length=1000,
        blank=True,
        help_text="Enter a brief description of the book.",
    )
    cover = models.ImageField(upload_to="covers/", blank=True)
    creator = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=["id"], name="id_index"),
        ]
        ordering = ["title"]
        permissions = [
            ("special_status", "Can read all books"),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])


class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    review = models.TextField("Review", blank=True)
    date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.review

    def get_absolute_url(self):
        return reverse("book_list")
