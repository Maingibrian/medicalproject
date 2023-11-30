from django.urls import path
from . import views

urlpatterns = [
    path("institutions/", views.institutions, name='institutions'),
    path("institutions/<str:pk>/", views.institution_details, name = "Institutions"),
    path('', views.main, name = "main"),
    path('Home2', views.Home2, name = "Home2"),
    path('home/', views.main, name = "main"),
    path('institution', views.institutions, name = 'institution'),
    path('new_institution/', views.new_institution, name='new_institution'),
    path('update_institution<str:pk>/', views.update_institution, name = 'update_institution'),
    path('delete_institution<str:pk>/', views.delete_institution, name = 'delete_institution'),
    path('admin_report', views.admin_report, name='admin_report'),
    path('auditorHome', views.auditorHome, name = "auditorHome"),
    path('delete_med_distribution/<str:pk>/', views.delete_med_distribution, name='delete_med_distribution'),
]