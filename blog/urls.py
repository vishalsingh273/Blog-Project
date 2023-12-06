
from django.urls import path
from .views import blog_detail,blog_list,like_blog,like_comment,login_required,comment_on_blog,share_blog
from .views import SignUpView ,CustomLoginView
from django.contrib.auth.views import LogoutView
urlpatterns = [
   
    path('', blog_list, name='blog_list'),
    path('blogs/<int:blog_id>/', blog_detail, name='blog_detail'),
    path('blogs/<int:blog_id>/like/', like_blog, name='like_blog'),
    path('blogs/<int:blog_id>/comment/', comment_on_blog, name='comment_on_blog'),
    path('comments/<int:comment_id>/like/', like_comment, name='like_comment'),
    path('blogs/<int:blog_id>/share/', share_blog, name='share_blog'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
     path('login/', CustomLoginView.as_view(), name='login'),
]




