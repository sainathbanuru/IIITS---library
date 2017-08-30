from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index.as_view(), name="adminIndex"),
    url(r'^issue/$', views.issue.as_view(), name="issue"),
    url(r'^add_book/$', views.add_book.as_view(), name="add_book"),
    url(r'^bookList/$', views.bookList.as_view(), name="bookList"),

]