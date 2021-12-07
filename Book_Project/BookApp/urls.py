from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('logout/', logout, name='logout'),
    path('add_product_page/', add_product_page, name='add_product_page'),
    path('add_product/', add_product, name='add_product'),
    path('product_detail/<int:pk>/',product_detail,name='product_detail'),
    path('product_edit/<int:pk>/', product_edit, name='product_edit'),
    path('product_delete/<int:pk>/', product_delete, name='product_delete'),
    path('user_product_detail/<int:pk>/', user_product_detail, name='user_product_detail'),
    path('user_view_product/<str:bn>/', user_view_product, name='user_view_product'),
    path('register/', register, name='register'),
    path('verify_otp/', otp, name='verify_otp'),
    path('add_to_wishlist/<int:pk>/',add_to_wishlist,name='add_to_wishlist'),
    path('add_to_cart/<int:pk>/',add_to_cart,name='add_to_cart'),
    path('remove_from_wishlist/<int:pk>/',remove_from_wishlist,name='remove_from_wishlist'),
    path('remove_from_cart/<int:pk>/',remove_from_cart,name='remove_from_cart'),
    path('mywishlist/',mywishlist,name='mywishlist'),
    path('mycart/',mycart,name='mycart'),
    path('update-cart/<int:pk>',update_cart,name='update-cart'),
    path('user-profile/',update_user,name='user-profile'),
    #path('update-user/',update_user,name='update-user'),

    # payment
    path('pay/', initiate_payment, name='pay'),
    path('callback/', callback, name='callback'),

    # user api
    #path('user-api/')
]