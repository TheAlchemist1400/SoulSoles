from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name = 'shop'),
    path('sneaker/<int:pk>/', views.sneaker_detail, name='sneaker_detail'),
    path('add-to-cart/<int:size_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', auth_views.LoginView.as_view(), name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('register/', views.register_view, name = 'register'),
    path('profile/', views.profile_view, name='profile'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('sourcing/', views.sourcing, name = 'sourcing'),
    path('checkout-successful/<int:order_id>/', views.checkout_successful, name = 'checkout_successful'),
    path('orders/', views.account_orders, name = 'account_orders'),
]
