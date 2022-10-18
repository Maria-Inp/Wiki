from django.urls import path

from . import views
app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("newEntry", views.newEntry, name="newEntry"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("random", views.randomPage, name="randomPage")
]
