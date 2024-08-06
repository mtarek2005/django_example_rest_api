from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('user/<int:pk>/', views.user_get),
    path('user/<int:pk>/get-posts', views.user_list_posts),
    path('user/<int:pk>/get-following', views.user_list_following),
    path('user/<int:pk>/get-followers', views.user_list_followers),
    path('post/<int:pk>/', views.post_get),
    path('post/<int:pk>/view', views.post_view),
    path('post/<int:pk>/reply', views.post_create_reply),
    path('post/<int:pk>/get-replies', views.post_list_replies),
    path('post/<int:pk>/like', views.post_create_like),
    path('post/<int:pk>/unlike', views.post_remove_like),
    path('post/<int:pk>/delete', views.post_delete),
    path('post/create', views.posts_create_post),
    path('post/upload-image', views.uploadImage),
    path('user/follow', views.user_follow),
    path('user/unfollow', views.user_unfollow),
    path('user/get-feed', views.user_get_feed),
    path('user/update-bio', views.user_update_bio),
]