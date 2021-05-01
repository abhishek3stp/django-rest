from django.urls import path
from knox import views as knox_views
from .views import LoginAPI, RegisterAPI
from . import views

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('moderator/', views.moderator, name='moderator'),
    path('detail/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('update/<str:slug>/', views.update, name='update'),
    path('delete/<str:slug>/', views.delete, name='delete'),
]
