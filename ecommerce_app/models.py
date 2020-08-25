from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.TextField()
    password = models.CharField(max_length=64)

class Category(models.Model):
    category = models.CharField(max_length=255)

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    description = models.TextField()
    categories = models.ManyToManyField(
        Category,
        related_name="products"
    )
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    # img = models.ImageField()

class Review(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="reviews",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    products = models.ManyToManyField(
        Product,
        related_name="carts",
    )
    user = models.ForeignKey(
        User,
        related_name="carts",
        on_delete=models.CASCADE
    )

class Order(models.Model):
    quantity_ordered = models.IntegerField()

    purchased_user = models.ForeignKey(
        User,
        related_name="orders",
        on_delete=models.CASCADE
    )
    purchased_product = models.ForeignKey(
        Product,
        related_name="orders",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
