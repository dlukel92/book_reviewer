from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^users/(?P<id>\d+)$', views.show_user),
    url(r'^books$', views.books),
    url(r'^books/add$', views.show_add),
    url(r'^books/(?P<id>\d+)$', views.show_book),
    url(r'^add_process$', views.add_process),
    url(r'^delete_review$', views.delete_review),
    url(r'^logout$', views.logout)
]