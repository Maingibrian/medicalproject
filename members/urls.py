from django.urls import path
from members import views

urlpatterns = [
    path('login', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('register_user', views.register_user, name="register_user"),
    path('medication', views.medication, name = "medication"),
    path('new_med', views.new_med, name = 'new_med'),
    path('update_med/<int:pk>/', views.update_med, name='update_med'),
    path('delete_med/<int:pk>/', views.delete_med, name='delete_med'),
    path('delete_med_distributed/<int:pk>/', views.delete_med_distributed, name='delete_med_distributed'),
    path("user_page", views.user_page, name='user_page'),
    path("user_report", views.user_report, name='user_report'),
    path('user_update_distribution/<int:pk>/', views.user_update_distribution, name='user_update_distribution'),
    path('notifications', views.notifications, name='notifications'),
    path('mark_notification_as_read/<int:notification_id>/', views.mark_notification_as_read,
         name='mark_notification_as_read'),
    ]