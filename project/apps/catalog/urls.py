from django.urls import path


from . import views
from django.conf import settings
from django.urls import include 
app_name = "catalog"
urlpatterns = [
    path('', views.home, name='home'),
    path('group/<int:id>/', views.topic_group, name='topic_group'),
    path('add_group/', views.add_group, name='add_group'),
    path('eliminate_post/', views.eliminate_post, name='eliminate_post'),
    path('edit_post/', views.edit_post, name='edit_post'),
    path("ia/" , views.ia , name="ia"),
    path("ia_response/" , views.ia_response , name="ia_response"),
    path("search/<int:page_number>", views.search_view, name="search_view"),
    path("rate_group/", views.rate_group, name="rate_group"),
    path("subscribe/", views.subscribe, name="subscribe"),
   
    
]

