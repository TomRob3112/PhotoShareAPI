from django.conf.urls import patterns, url

from PhotoSharingApplication.APIS import user_manager_api, categories_api_manager, picture_manager_api
from PhotoSharingApplication import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login_action', user_manager_api.login_action, name='login_action'),
    url(r'^logout_action', user_manager_api.logout_action, name='logout_action'),
    url(r'^register_action', user_manager_api.register_action, name='register_action'),

    url(r'^login', views.login, name='login'),
    url(r'^home', views.home, name='home'),
    url(r'^register', views.register, name='register'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^category_list', views.category_list, name='category_list'),


    url(r'^facebooklogin', user_manager_api.facebook_login, name='facebooklogin'),
    url(r'^get_all_categories', categories_api_manager.get_all_categories, name='get_all_categories'),
    url(r'^get_pictures_for_category', categories_api_manager.get_pictures_for_category, name='get_pictures_for_category'),
    url(r'^like', picture_manager_api.like, name='like'),
    url(r'^abuse_picture', picture_manager_api.abuse_picture, name='abuse_picture'),


)