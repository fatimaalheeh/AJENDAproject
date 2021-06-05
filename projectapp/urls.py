from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login',views.login),
    path('register', views.register),
    path('registration',views.registration),
    path('profile',views.profile),
    path('logout',views.logout),
    path('update',views.update),
    path('success/<int:id>',views.success),
    path('main',views.main)
    # path('main',views.main),
]