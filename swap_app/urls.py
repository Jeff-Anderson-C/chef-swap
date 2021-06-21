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
    path('create_sugg/<int:rec_id>', views.create_sugg),
    path('my_suggs', views.my_suggs),
    path('sugg_for_me/<int:rec_id>', views.sugg_for_me),
    path('destroy_sugg/<int:sugg_id>', views.delete_sugg),
    path('favRecipes', views.fav_recipes),
    path('make_fav/<int:rec_id>', views.make_fav),
    path('testKit', views.test_kit),
    path('knifeRoll', views.knife_roll),
]