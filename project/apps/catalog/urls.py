from django.urls import path


from . import views
from django.conf import settings
from django.urls import include 
# pip install djangorestframework-simplejwt 
from rest_framework_simplejwt.views import(TokenObtainPairView, TokenRefreshView, TokenVerifyView)
app_name = "catalog"
urlpatterns = [
    path('', views.home, name='home'),
    path('group/<int:id>/', views.topic_group, name='topic_group'),
    path('add_group/', views.add_group, name='add_group'),
    path('eliminate_post/', views.eliminate_post, name='eliminate_post'),
    path('edit_post/', views.edit_post, name='edit_post'),
    path("ia_response/" , views.ia_response , name="ia_response"),
    path("search/", views.search_view, name="search_view"),
    path("search_view_post/", views.search_view_post, name="search_view_post"),
    path("rate_group/", views.rate_group, name="rate_group"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("obtener_input_video/", views.obtener_input_video, name="obtener_input_video"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    
]

