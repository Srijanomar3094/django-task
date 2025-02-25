from django.urls import path
from .views import *


### Task-2 API's As recomended with usage of Frontend(Next.js)
 
urlpatterns = [
    path("register/", user_register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("roles/", user_roles, name="roles"),
    path("routes/", left_panel, name="leftpanel"),
    path("profile/", profile_data, name="profile"),
    path("blogs/", blog_list, name="blog_list"),
    path("blogs/create/", create_blog, name="create_blog"),
    path("blogs/my/", my_blogs, name="my_blogs"),
    path("blogs/<int:blog_id>/", blog_detail, name="blog_detail"),
    path("categories/", get_blog_categories, name="get_blog_categories"),
]
