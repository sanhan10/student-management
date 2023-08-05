from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from snap import views
from snap.views import admin_dashboard_view, admin_404, admin_password_reset,add_registration_view,delete_multiple_registrations_view, list_registration_view, update_registration_view, delete_registration_view

urlpatterns = [
    path('', views.index, name='index'),
    path('adminclick/', views.adminclick_view, name='adminclick'),
    path('adminlogin/', LoginView.as_view(template_name='admin/login.html'), name='adminlogin'),
    path('afterlogin/', views.afterlogin_view, name='afterlogin'),
    path('logout/', LogoutView.as_view(next_page='/adminlogin/'), name='logout'),
    path('admin-dashboard/', admin_dashboard_view, name='admin-dashboard'),
    path('add-registration/', add_registration_view, name='add-registration'),
    path('list-registration/', list_registration_view, name='list-registration'),
  
    path('update-registration/<int:registration_id>/', update_registration_view, name='update-registration'),
    path('delete-registration/<int:registration_id>/', delete_registration_view, name='delete-registration'),
     path('delete-multiple-registrations/', delete_multiple_registrations_view, name='delete-multiple-registrations'),
      path('admin/password/reset/', admin_password_reset, name='admin_password_reset'),
    # ... other URL patterns ...
   
    path('admin/404/', admin_404),
    path('', include("snap.urls")),
]
