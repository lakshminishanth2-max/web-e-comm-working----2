from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('product/<int:id>/', views.product_detail),
    path('cart/', views.cart_view),
    path('cart/<int:id>/', views.add_to_cart),
    path('login/', views.login_view),
    path('checkout/', views.checkout),
    path('success/', views.success),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('add-wishlist/<int:product_id>/', views.add_wishlist),
    path('rate/<int:product_id>/', views.add_rating),
    path('orders/', views.orders, name="orders"),
    path('order/<int:product_id>/', views.place_order),
    path('pay/<int:product_id>/', views.payment),
]