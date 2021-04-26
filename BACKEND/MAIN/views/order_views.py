from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from MAIN.models import Product, Order, OrderItem, ShippingAddress
from MAIN.serializers import ProductSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from datetime import datetime


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrder(request):
    user = request.user
    pk = request.query_params.get("pk")
    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or user == order.user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            message = {
                "message": "Why are you trying to view your friend's order"}
            return Response(message, status=status.HTTP_403_FORBIDDEN)
    except:
        message = {"message": "I couldnt find this order anywhere"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrders(request):
    user = request.user
    type = request.query_params.get("type")
    page = request.query_params.get("page")
    if type == "all":
        if user.is_staff:
            orders = Order.objects.all()
        else:
            message = {"message": "Only I can see all orders"}
            return Response(message, status=status.HTTP_403_FORBIDDEN)
    elif type == "mine":
        orders = Order.objects.get(user=user)

    paginator = Paginator(orders, 10)
    if page == None:
        page = 1
    try:
        orders = paginator.page(page)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    page = int(page)
    serializer = OrderSerializer(orders, many=True)
    return Response({"orders": serializer.data, "page": page, "pages": paginator.num_pages})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editOrder(request):
    type = request.query_params.get("type")
    pk = request.query_params.get("pk")
    user = request.user
    if type == "delivered":
        if user.is_staff:
            order = Order.objects.get(_id=pk)
            order.isDelivered = True
            order.deliveredAt = datetime.now()
            order.save()
            message = {"message": "One order less to bother about"}
            return Response(message)
        else:
            message = {"message": "Did you really delliver this order?"}
            return Response(message, status=status.HTTP_403_FORBIDDEN)
    elif type == "paid":
        order = Order.objects.get(_id=pk)
        if order.user == user:
            order.isPaid = True
            order.paidAt = datetime.now()
            order.save()
            message = {"message": "Thanks for paying this order"}
            return Response(message)
        else:
            message = {"message": "You cant pay your friend's order!"}
            return Response(message, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createOrder(request):
    user = request.user
    data = request.data
    orderItems = data['orderItems']
    if orderItems and len(orderItems) == 0:
        message = {"message": "You wanna buy nothing in the shop of nothing?"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        order = Order.objects.create(
            user=user,
            totalPrice=data['totalPrice'],
            shippingPrice=data['shippingPrice'],
            taxPrice=data['taxPrice'],
            paymentMethod=data['paymentMethod'],
        )
        shippingAddress = ShippingAddress.objects.create(
            order=order,
            address=data["shippingAddress"]["address"],
            city=data["shippingAddress"]["city"],
            country=data["shippingAddress"]["country"],
            postalCode=data["shippingAddress"]["postalCode"],
            shippingPrice=data["shippingAddress"]["shippingPrice"]
        )
        for item in orderItems:
            product = Product.objects.get(id=item['product'])
            item = OrderItem.objects.create(
                product=product,
                order=order,
                qty=item['qty'],
                # image=product.image.url,
            )
            # update product stock
            product.countInStock -= item.qty
            product.timesSold += item.qty
            product.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
