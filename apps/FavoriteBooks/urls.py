from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^user/new$', views.create),
    url(r'^load$', views.load),
    url(r'^login$', views.login),
    url(r'^logOut$', views.logOutUser),
    
    url(r'^books/create$', views.createBook),
    url(r'^books/(?P<idBook>\d+)$', views.showFor),
    url(r'^addFavorite/(?P<idBook>\d+)$', views.addFavorite),
    url(r'^books/update/(?P<idBook>\d+)$', views.updateBook),
    url(r'^books/delete/(?P<idBook>\d+)$', views.deleteBook),
    url(r'^unFavorite/(?P<idBook>\d+)$', views.unFavorite),
        
]