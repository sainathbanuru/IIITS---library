from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index.as_view(), name="index"),
    url(r'^issue_book/$', views.issue_book.as_view(), name="issue_book"),
    url(r'^book_return/$', views.book_return.as_view(), name="book_return"),

    url(r'^add_book/$', views.add_book.as_view(), name="add_book"),
    url(r'^bookList/$', views.bookList.as_view(), name="bookList"),
    url(r'^bookUpdate/$', views.bookUpdate.as_view(), name="bookUpdate"),
    url(r'^bookDetails/(?P<accn>[0-9]+)/$', views.bookDetailsUpdate, name="bookDetailsUpdate"),
    url(r'^ajax/autocomplete/$', views.autocomplete, name='ajax_autocomplete'),

]