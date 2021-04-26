from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from MAIN.serializers import ProductSerializer
from MAIN.models import Product
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import operator


@api_view(['GET'])
def getProduct(request):
    pk = request.query_params.get("pk")
    product = Product.objects.get(id=pk)
    serializer = PorductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getProducts(request):
    type = request.query_params.get("type")
    page = request.query_params.get("page")
    if type == "search":
        query = request.query_params.get("query")
        products = Product.objects.filter(name__icontains=query)
        ordered = sorted(products, key=operator.attrgetter("rating"))
        paginator = Paginator(ordered, 5)
        if page == None:
            page = 1
        try:
            products = paginator.page(page)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        page = int(page)
        serializer = ProductSerializer(products, many=True)
        return Response({"products": serializer.data, "page": page, "pages": paginator.num_pages})

    elif type == "category":
        products = Product.objects.filter(category=which)
        ordered = sorted(products, key=operator.attrgetter("rating"))
        paginator = Paginator(ordered, 5)
        if page == None:
            page = 1
        try:
            products = paginator.page(page)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        page = int(page)
        serializer = ProductSerializer(products, many=True)
        return Response({"products": serializer.data, "page": page, "pages": paginator.num_pages})

    elif type == "top":
        by = request.query_params.get("by")
        count = request.query_params.get("count")
        if by == "rating" or by == "timesSold" or by == "discountPercent":
            produts = Product.objects.order_by(by)[:count]
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        elif by == "category":
            which = request.query_params.get("which")
            products = Product.objects.filter(category=which)[:count]
            ordered = sorted(products, key=operator.attrgetter("rating"))
            serializer = ProductSerializer(ordered, many=True)
            return Response(serializer.data)
        else:
            message = {"message": "What kind of top do you want"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    message = {"message": "Im stupid, you need to be more specific"}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def editProduct(request):
    # imma add "add review"
    pk = request.query_params.get("pk")
    if pk != "":
        data = request.data
        product = Product.objects.get(id=pk)
        product.name = data["name"]
        product.shortName = data["shortName"]
        #product.image = data["image"]
        product.price = data["price"]
        product.discountPercent = data["discountPercent"]
        product.countInStock = data["countInStock"]
        product.brand = data["brand"]
        product.category = data["category"]
        product.description = data["description"]
        product.adicional = data["adicional"]
        product.save()
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    else:
        message = {"message": "You have to specify what product"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    type = request.query_params.get("type")
    data = request.data
    if type == "product":
        try:
            product = Product.objects.create(
                name=data["name"],
                shortName=data["shortName"],
                #image = data["image"]
                price=data["price"],
                discountPercent=data["discountPercent"],
                countInStock=data["countInStock"],
                brand=data["brand"],
                category=data["category"],
                description=data["description"],
                adicional=data["adicional"]
            )
            serializer = ProductSerializer(product, many=False)
            return Response(serializer.data)
        except:
            message = {
                "message": "There was an error making this product, please try again"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    elif type == "review":
        pk = request.query_params.get("pk")
        user = request.user
        product = Product.objects.get(_id=pk)
        alreadyExists = product.review_set.filter(user=user).exists()
        if alreadyExists:
            message = {"message": "You already made a review for this product"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        elif data['rating'] == 0:
            message = {"message": "Please select a rating"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        # create review
        else:
            review = Review.objects.create(
                user=user,
                product=product,
                rating=data["rating"],
                review=data["review"],
                miniReview=str(data["review"])[:10] + "..."
            )
            reviews = product.review_set.all()
            product.numReviews = len(reviews)
            total = 0
            for i in reviews:
                total += i.rating
            product.rating = total / len(reviews)
            product.save()
            message = {
                "message": "Your constructive review was posted successfully"}
            return Response(message)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request):
    pk = request.query_params.get("pk")
    product = Product.objects.get(id=pk)
    name = product.name
    product.delete()
    message = {"message": "The product " +
               name + " was successfully terminated"}
    return Response(message)
