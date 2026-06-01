# urls.py

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index_view, name='index'), 
    path('contact/', views.contact_view, name='contact'),
    path('prediction/', views.prediction_view, name='prediction'),
    path('signup/', views.user_signup_view, name='user_signup'),
    path('login/', views.user_login_view, name='user_login'),
    path('logout/', views.user_logout_view, name='user_logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('about/',views.about_view,name='about'),
    path('Home/',views.HomePage,name='Home'),
    # urls.py
    path('Dashboard/', views.dashboard, name='dashboard'),

    
]