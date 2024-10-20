from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.tasks import send_order_confirmation_email
from apps.api.models import Order, Product
from apps.api.serializers import (
    OrderSerializer, OrderUserDetailSerializer,
    AddProductSerializer, RemoveProductSerializer,
)

class OrdersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(customer=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(Order.STATUS_CHOICES.CREATED)
        order = Order.objects.create(
            customer=request.user, 
            status=Order.STATUS_CHOICES.CREATED, 
            total_price=0)
        return Response({"order_id": order.id}, status=status.HTTP_201_CREATED)

class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        order = Order.objects.get(pk=pk, customer=request.user)
        serializer = OrderUserDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderAddProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        serializer = AddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = Order.objects.get(pk=pk, customer=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            product = Product.objects.get(pk=serializer.validated_data['product_id'])
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        order.add_product(product, serializer.validated_data['quantity'])
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderRemoveProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        serializer = RemoveProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = Order.objects.get(pk=pk, customer=request.user)
        product = Product.objects.get(pk=serializer.validated_data['product_id'])
        order.remove_product(product, serializer.validated_data['quantity'])
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderRemoveAllProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        order = Order.objects.get(pk=pk, customer=request.user)
        order.remove_all_products()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        order = Order.objects.get(pk=pk, customer=request.user)
        order.process_payment()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderDeliveryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        order = Order.objects.get(pk=pk, customer=request.user)
        order.ship_order()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderFinishView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        order = Order.objects.get(pk=pk, customer=request.user)
        
        order.finish_order()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        order = Order.objects.get(pk=pk, customer=request.user)
        order.cancel_order()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderFinishViewEmailConf(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, customer=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        user_email = order.customer.email  
        order_id = order.id  

        try:
            send_order_confirmation_email.delay(order_id, user_email)
        except Exception as e:
            return Response({"detail": "Failed to send confirmation email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        order.finish_order()

        return Response(status=status.HTTP_204_NO_CONTENT)