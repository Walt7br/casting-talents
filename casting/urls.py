from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('talents/', views.talent_list, name='talent_list'),
    path('talents/new/', views.talent_create, name='talent_create'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/new/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/roles/new/', views.role_create, name='role_create'),
    path('applications/', views.application_list, name='application_list'),
    path('applications/new/', views.application_create, name='application_create'),
    path('applications/<int:pk>/status/<str:status>/', views.application_update_status, name='application_update_status'),
    path('schedule/', views.schedule_list, name='schedule_list'),
    path('schedule/new/', views.schedule_create, name='schedule_create'),
]
