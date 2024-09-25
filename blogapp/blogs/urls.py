from django.urls import path
from . import views


urlpatterns = [
    #path('', views.index, name='index' ),
    path('', views.BlogListView.as_view(), name = 'blog_list'),
    path('create/', views.BlogCreateView.as_view(), name = 'blog_create'),
    path('<int:blog_id>/edit/', views.BlogUpdateView.as_view(), name = 'blog_edit'),
    path('<int:blog_id>/delete/', views.BlogDeleteView.as_view(), name = 'blog_delete'),
    path('register/', views.RegisterView.as_view(), name = 'blog_register'),
]
