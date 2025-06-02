from django.urls import path
from StripeApp import views

urlpatterns = [
    path('item/<int:item_id>/', views.get_item, name='get_item'),
    path('buy/<int:item_id>/', views.buy_item, name='buy_item'),
    path('cancel/', views.cancel, name='cancel_page'),
    path('success/', views.success, name='success_page'),
    path('get-order/', views.show_order, name='show_order'),
    path('get-order/<int:order_id>/', views.show_order, name='show_order'),
    path('order/', views.get_order, name='get_order'),
    path('add-to-order/', views.add_to_order, name='add_to_order'),
    path('buy/order/<int:order_id>/', views.buy_order, name='buy_order'),
]
