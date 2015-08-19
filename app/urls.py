"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from showmeyoutube import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home', views.home, name="home"),
    url(r'^register$', views.register, name = "register"),
    url(r'^login$', views.login_, name = 'login'),
    url(r'^registered', views.registered, name = 'registered'),
    url(r'^logged_in', views.logged_in, name = 'logged_in'),
    url(r'^logout', views.logout_, name = 'logout_'),
    url(r'^like$', views.like, name = 'like'),
    url(r'^likes$', views.load_likes, name = 'likes'),
    url(r'^history$', views.load_history, name = 'history'),
    url(r'^filters$', views.set_filters, name = 'filters'),
    url(r'^save_categories$', views.save_categories, name = 'save_categories'),
]
