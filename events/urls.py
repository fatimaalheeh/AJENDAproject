from django.urls import path,include
from . import views

urlpatterns = [
    path('event', views.test),
    path('details/<int:id>', views.details),
    path('add_event', views.add),
    path('delete/<int:id>', views.delete),
    path('edit_details/<int:id>', views.edit_details),
    path('save_details/<int:id>', views.save_details),
    path('attend/<int:id>', views.attended),
    path('cancel/<int:id>', views.cancel),
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
