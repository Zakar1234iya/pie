from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),   
    path('login', views.login ,  name='logout'),
    path('logout', views.logout),
    path('dashboard', views.profile, name='dashboard'),
    path('add_pie', views.add_pie),
    path('pies', views.view_pie, name='all_pies'),
    path('pies/<int:id>', views.view_pies, name='view_pies'),
    path('pies/edit/<int:id>', views.edit_pie, name='edit_pie'),
    path('pies/delete/<int:id>', views.delete_pie, name='delete_pie'),
    path('update_pie', views.update_pie, name='update_pie'),
    path('upvote', views.incvote, name='upvote'),  
    path('downvote', views.decvote, name='downvote'),  
]
