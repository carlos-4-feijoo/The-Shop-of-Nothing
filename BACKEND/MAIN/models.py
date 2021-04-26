from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    shortName = models.CharField(max_length=50, null=True, blank=True)
    #image = models.ImageField(null=True, blank=True, default='/sample.jpg')

    rating = models.DecimalField(
        max_digits=2, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)

    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    discountPercent = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)
    countInStock = models.IntegerField(null=True, blank=True, default=0)

    createdAt = models.DateTimeField(auto_now_add=True)

    timesSold = models.IntegerField(null=True, blank=True, default=0)

    # DESCRIPCION
    brand = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    # opcionales

    #costums: "atributo:valor-atributo:valor"
    adicional = models.CharField(
        max_length=100, null=True, blank=True, default="")

    def __str__(self):
        return str(self.name)


empty = " " * 10


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    review = models.TextField(null=True, blank=True, default=empty)
    miniReview = models.TextField(
        null=True, blank=True, default=str(review)[0:9] + "...")
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.miniReview)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    totalPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    isDelivered = models.BooleanField(default=False)
    # TIME
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    deliveredAt = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    # OTHER
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    taxPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    paymentMethod = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.user)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.order)


class ShippingAddress(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.address)
