from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index),
    path('log_reg', views.log_reg),
    path('register', views.register),
    path('login', views.login),
    
    path('dash', views.dash),
    path('logout', views.logout),
    path('new_rec', views.new_rec),
    path('create_new', views.create_new),
    path('my_recipes', views.my_recipes),
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
    path('fav_recipes', views.fav_recipes),
    path('make_fav/<int:rec_id>', views.make_fav),
    path('search_recipes', views.search_recipes),
    path('photo_up', views.photo_up),
    path('change_pic/<int:rec_id>', views.change_pic),
    path('group_recs', views.group_recs),

    path('test_kit', views.test_kit),
    path('new_test_rec', views.new_test_rec),
    path('view_test_rec/<int:rec_id>', views.view_test_rec),
    path('save_test_rec', views.save_test_rec),
    path('save_test_rec_edit/<int:rec_id>', views.save_test_rec_edit),
    path('save_to_main/<int:test_id>', views.save_to_main),


    path('prof_dash', views.prof_dash),
    path('pr_photo_up', views.pr_photo_up),
    path('kr_photo_up', views.kr_photo_up),
    path('add_text_post', views.add_text_post),
    path('add_post', views.add_post),
    path('post_content', views.post_content),
    path('my_profile', views.my_profile),
    path('profile_edit_save', views.profile_edit_save),
    path('roll_manage', views.roll_manage), 
    path('groups', views.groups), 
    path('view_group/<int:group_id>', views.view_group),
    path('view_image/<int:img_id>', views.view_image),
    path('destroy_image/<int:img_id>', views.destroy_image),
    path('destroy_post/<int:post_id>', views.destroy_post),


    path('create_group', views.create_group),
    path('join_request/<int:group_id>', views.join_request),
    path('search_chefs', views.search_chefs),
    path('other_prof/<int:chef_id>', views.other_prof),
    path('accept_member/<int:invite_id>', views.accept_member),
    path('reject_member/<int:invite_id>', views.reject_member),
    path('destroy_acct/<int:user_id>', views.destroy_acct),

    path('contact', views.contact), 
    path('terms_conditions', views.terms_conditions),
    path('privacy_policy', views.privacy_policy),
]