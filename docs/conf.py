"""Sphinx configuration."""

project = "bookstore"
author = "Kevin Bowen"
copyright = f"2024, {author}"
#
html_theme = "furo"
html_logo = "django_24.png"
html_title = "bookstore"
extensions = [
    "sphinx.ext.duration",
]
