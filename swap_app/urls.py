from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dash', views.dash),
    path('logout', views.logout),
    path('new_rec', views.new_rec),
    path('create_new', views.create_new),
    path('myRecipes', views.myRecipes),
    path('recipe/<int:rec_id>', views.recipe),
    path('all_rec', views.all_rec),
    path('edit/<int:rec_id>', views.edit_rec),
    path('save_edit/<int:rec_id>', views.save_edit),
    path('destroy/<int:rec_id>', views.remove_rec), 
    path('suggest/<int:rec_id>', views.suggest),
    path('create_sugg', views.create_sugg),
]