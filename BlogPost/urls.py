from django.urls import path
from . import views
urlpatterns = [
    path('',views.createblog,name='createblog'),
    path('my-posts/', views.my_blog_posts, name='my_blog_posts'),
]