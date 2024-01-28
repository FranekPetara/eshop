from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from product.models import Product
from .serializer import OrderSerializer

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many= True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    serializer = OrderSerializer(order, many= False)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):

    user = request.user
    data = request.data

    order_items = data['orderItems']

    if order_items and len(order_items) == 0:
        return Response({'error': "No order items"}, status=status.HTTP_400_BAD_REQUEST)
    else:

        #create order

        total_amount = sum(item['price'] * item['quantity'] for item in order_items)

        order = Order.objects.create(
            user=user,
            street = data['street'],
            city = data['city'],
            state = data['state'],
            zip_code = data['zip_code'],
            phone_no = data['phone_no'],
            country = data['country'],
            total_amount = total_amount,
            )
        
        for order_item in order_items:

            product = Product.objects.get(id=order_item['product'])
            item = OrderItem.objects.create(
                product = product,
                orders = order,
                name = product.name,
                quantity = order_item['quantity'],
                price = order_item['price']
            )

        product.stock -= item.quantity
        product.save()

    serializer = OrderSerializer(order, many = False)
    return Response(serializer.data)

