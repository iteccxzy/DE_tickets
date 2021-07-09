from django.urls import path
from entry import views

urlpatterns = [

    path('register', views.registerPage, name='register'),
    path('login', views.loginPage, name = 'login'),
    path('logout', views.logoutUser, name = 'logout'),

    path('', views.getProfile, name = 'profile'),
    path('edit/', views.edit, name = 'edit'),

    path('get_plans/<int:id>', views.get_plans, name='get_plans'),
    path('get_stocks/<int:id>', views.get_stocks, name='get_stocks'),
    path('get_orders/<int:id>', views.getOrder, name='get_orders'),

    path('set_plans', views.set_plans, name='set_plans'),
    path('add_orders', views.add_orders, name='add_orders'),
    path('delete_order/<int:id>', views.delete_order, name='delete_order'),

    path('customer/<int:id>', views.customer_view, name = 'customer'),
    path('get_date', views.get_date, name = 'get_date'),
    path('get_time', views.get_time, name = 'get_time'),
    path('save_customer', views.save_customer, name = 'save_customer'),
    path('add_customer_or', views.add_customer_or, name = 'add_customer_or'),
   
    path('customer', views.cus_view, name = 'cus'),
    path('my-ticket', views.my_ticket, name = 'my-ticket'),
    
   ]