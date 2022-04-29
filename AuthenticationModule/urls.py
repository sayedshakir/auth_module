
import imp
from . import views
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from django.views.generic import TemplateView


urlpatterns = [
    path('', views.home, name="home"),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    

    path('register', views.register, name="register"),
    
    path('logout', views.logoutt, name="logoutt"),
    path('loggedin', views.loggedin, name="loggedin"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('login', views.loginn, name="loginn"),

    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    
]