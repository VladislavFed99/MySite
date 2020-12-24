"""
Definition of urls for MySite.
"""

from datetime import datetime
from django.urls import path, include
from django.contrib import admin

from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from app import forms, views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Вход в аккаунт',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('registration/', views.registration, name='registration'),
    path('news/', views.blog, name='blog'),
    path('(<parametr>)', views.blogpost, name='blogpost'),
    path('newpost/', views.newpost, name='newpost'),
    path('catalog/', views.catalog, name='catalog'),

    path('(<category_slug>)/', views.catalog, name='product_list_by_category'),
    path('(<id>)/(<slug>)', views.product, name='product'), 

    path('myorders/', views.account, name='account'),
    path('myorder/<param>', views.accountorder, name='accountorder'),

    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<product_id>/', views.cart_add, name='cart_add'),
    path('remove/<product_id>/', views.cart_remove, name='cart_remove'),

    path('create/', views.order_create, name='order_create'),

    path('favicon.ico',
        RedirectView.as_view(
            url=staticfiles_storage.url('favicon.ico'), permanent=False),
        name="favicon"
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
