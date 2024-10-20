from django.urls import path
from .views import (
    OrdersView,
    OrderDetailView,
    OrderAddProductView,
    OrderRemoveProductView,
    OrderRemoveAllProductView,
    OrderPaymentView,
    OrderDeliveryView,
    OrderFinishView, OrderFinishViewEmailConf,
    OrderCancelView,
    
    ProductList, ProductDetail,
    CategoryList, CategoryDetail
)

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='orders-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/add-product/', OrderAddProductView.as_view(), name='order-add-product'),
    path('orders/<int:pk>/remove-product/', OrderRemoveProductView.as_view(), name='order-remove-product'),
    path('orders/<int:pk>/remove-all-products/', OrderRemoveAllProductView.as_view(), name='order-remove-all-products'),
    path('orders/<int:pk>/payment/', OrderPaymentView.as_view(), name='order-payment'),
    path('orders/<int:pk>/delivery/', OrderDeliveryView.as_view(), name='order-delivery'),
    path('orders/<int:pk>/finish/', OrderFinishViewEmailConf.as_view(), name='order-finish'),
    path('orders/<int:pk>/cancel/', OrderCancelView.as_view(), name='order-cancel'),

    path("products/", ProductList.as_view(),  name='product-list'),
    path("products/<int:pk>/", ProductDetail.as_view(), name='product-detail'),

    path("categories/", CategoryList.as_view(),  name='category-list'),
    path("categories/<int:pk>/", CategoryDetail.as_view(), name='category-detail'),
]
