from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import (NewsDetailView, AboutUs, AllRestaurant, Contact,
                    MainView, News, SearchPost, AuthUserView, RegisterUserView, UserLogout, activate)

urlpatterns = [
    path('', MainView.as_view(), name='base'),
    path('news', News.as_view(), name='news'),
    path('all-restaurant', AllRestaurant.as_view(), name='all-restaurant'),
    path('about-us', AboutUs.as_view(), name='about-us'),
    path('contact', Contact.as_view(), name='contact'),
    path('post/<int:pk>', NewsDetailView.as_view(), name='news-detail'),
    path('search-result', SearchPost.as_view(), name='search-result'),
    path('login/', AuthUserView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('review/<int:pk>/', NewsDetailView.as_view(), name="add_review"),


    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html'), name='reset_password'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_sent.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_form.html'), name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_complete'),
]
