from django.urls import path, include
from django.contrib import admin
from myapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('book/<int:service_id>/', views.show_booking_form, name='show_booking_form'),
    path('book/appointment/', views.book_appointment, name='book_appointment'),

    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/bookings/', views.manage_bookings, name='manage_bookings'),
    path('admin/bookings/edit/<int:id>/', views.edit_booking, name='edit_booking'),
    path('admin/bookings/delete/<int:id>/', views.delete_booking, name='delete_booking'),
    path('admin/services/', views.manage_services, name='manage_services'),
    path('admin/services/edit/<int:id>/', views.edit_service, name='edit_service'),
    path('admin/services/delete/<int:id>/', views.delete_service, name='delete_service'),
    path('admin/customers/', views.manage_customers, name='manage_customers'),
    path('admin/customers/edit/<int:id>/', views.edit_customer, name='edit_customer'),
    path('admin/customers/delete/<int:id>/', views.delete_customer, name='delete_customer'),

    path('admin/', admin.site.urls),
]
