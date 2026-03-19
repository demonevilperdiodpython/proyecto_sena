from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.Register_view, name='singup'),
    path('acounts/', views.acounts_view, name='acounts'),  
    path('logout/', views.logOut_view, name='logout'), 
    path('eliminate_session/<int:user_id>/', views.eliminate_user_session_view, name='eliminate_user_session'),
    path('loginwith', views.log_in_with_user_view, name='login_with_user'),
]
