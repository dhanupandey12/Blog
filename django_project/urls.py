from django.contrib import admin
from django.urls import path
from blog.views import PostListView, PostCreateView, PostUpdateView, PostDeleteView
from users import views as userViews
from blog import views as Blogviews
from django.contrib.auth import views as authViews
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/',admin.site.urls),
    path('', Blogviews.home, name='blog-home'),
    path('post/<int:pk>/', Blogviews.postDetail, name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('trendingPost/', Blogviews.trendingPost, name='blog-trend'),
    path('reportPost/<int:pk>', Blogviews.reportPost, name='report'),
    path('likePost/<int:pk>', Blogviews.likePost, name='like-post'),
    path('hatePost/<int:pk>', Blogviews.hatePost, name='hate-post'),

    path('register/',userViews.register,name='register'),
    path('login/',authViews.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',authViews.LogoutView.as_view(template_name='users/logout.html'),name='logout'), 
    
    path('password-reset/',authViews.PasswordResetView.as_view(template_name='users/password_reset.html'),name='password_reset'), 
    path('password-reset/done/',authViews.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'), 
    path('password-reset-confirm/<uidb64>/<token>',authViews.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',authViews.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),  
    path('profile/',userViews.profile,name='profile'),
    path('updateProfile/',userViews.update,name='updateProfile'),
    path('user/<int:pk>/', userViews.UserProfileView, name='user-profile'),
    path('allUsers/', Blogviews.about, name='blog-about'),
    path('message/<int:pk>',userViews.storeMessage,name='message'),
    path('detailMessage/<int:pk>',userViews.detailedMessage,name='detail-message'),
    path('checkMessage/',userViews.checkMessage,name='checkMessage'),
    path('reviews/',Blogviews.getReviews,name='reviews'),
    path('reviews/add',Blogviews.postReviews,name='add-reviews'),
    path('message/',userViews.messageSummary,name='message-summary'),
    path('addFriend/<int:pk>',userViews.addFriend,name='add-friend'),
    path('removeFriend/<int:pk>',userViews.removeFriend,name='remove-friend'),
    path('friends/',userViews.myFriends,name='my-friend'),
    path('followers/',userViews.myFollowers,name='my-followers'),
    path('notifications/',userViews.myNotifications,name='my-notice'),
    path('search/',userViews.search,name='search'),
    path('verify/',userViews.verify,name='verify'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)