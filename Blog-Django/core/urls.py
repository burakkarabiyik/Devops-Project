"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib.staticfiles.storage import staticfiles_storage
from blogadmin.views import *
from django.views.generic.base import RedirectView
from django.views.static import serve

urlpatterns = [
    path('admin/', blogadmin, name="IndexAdmin"),
    path('', index, name='Index'),
    path('index/', index, name='Index'),
    path('about/', about, name='About'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('contact/', contact, name='Contact'),
    path('admin/articles/', products, name='Products'),
    path('admin/addarticle/', add, name='Add'),
    path('admin/edit/<str:value>', productdetails, name='edit'),
    path('admin/edit/', editsave, name='editsave'),
    path('admin/accounts/', accounts, name='accounts'),
    path('admin/accounts/<str:value>', accounts, name='accountsedit'),
    path('post/<slug:slug>/', postdetails, name='postdetails'),
    path('admin/deletemakale/', deletemakale, name='deletemakale'),
    path('admin/deletecategory/<str:categoryname>',
         deletecategory, name='deletecategory'),
    path('admin/addcategory/', addcategory, name='addcategory'),
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('favicon.ico'))),
    url(r'media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),

]
