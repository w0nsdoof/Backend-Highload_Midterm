from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    ProductList, ProductDetail,
    OrderList, OrderDetail,
    OrderItemList, OrderItemDetail
)
urlpatterns = [
    path("product/", ProductList.as_view(),  name='product_list'),
    path("product/<int:pk>/", ProductDetail.as_view(), name='product_detail'),

    path("order/", OrderList.as_view(),  name='order_list'),
    path("order/<int:pk>/", OrderDetail.as_view(), name='order_detail'),

    path("item/", OrderItemList.as_view(),  name='order-item_list'),
    path("item/<int:pk>/", OrderItemDetail.as_view(), name='order-item_detail'),
]