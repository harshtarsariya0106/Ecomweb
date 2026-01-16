from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='shop'),
    path('about/',views.about, name='about'),
    path('contact/',views.contact, name='contact'),
    path('tracker/',views.tracker, name='tracker'),
    path('productview/<int:id>/',views.productview, name='productview'),
    path('checkout/', views.checkout, name='checkout'),
    path('search/', views.search, name='search'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path("clear-cart/", views.clear_cart, name="clear_cart")

]
