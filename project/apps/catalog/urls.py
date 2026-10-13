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
    path('edit_group/<int:id>/', views.edit_group, name='edit_group'),
    path('eliminate_group/<int:id>/', views.eliminate_group, name='eliminate_group'),
    path('group/<int:group_id>/add_section/', views.add_section, name='add_section'),
    path('group/<int:group_id>/section/<int:section_id>/', views.topic_section_view, name='topic_section'),
    path('group/<int:group_id>/section/<int:section_id>/post/', views.post_in_section, name='post_in_section'),
    path('edit_section/<int:group_id>/<int:section_id>/', views.edit_section, name='edit_section'),
    path('eliminate_section/<int:group_id>/<int:section_id>/', views.eliminate_section, name='eliminate_section'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('add_group/', views.add_group, name='add_group'),
    path('eliminate_post/', views.eliminate_post, name='eliminate_post'),
    path('edit_post/', views.edit_post, name='edit_post'),
    path("ia_response/" , views.ia_response , name="ia_response"),
    path("ia/", views.ia_view, name="ia"),
    path("settings/", views.settings_view, name="settings"),
    path("popular/", views.popular, name="popular"),
    path("search/", views.search_view, name="search_view"),
    path("search_view_post/", views.search_view_post, name="search_view_post"),
    path("rate_group/", views.rate_group, name="rate_group"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("obtener_input_video/", views.obtener_input_video, name="obtener_input_video"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    
]

