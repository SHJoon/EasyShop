from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if (len(postData['registered_first_name'])) == 0:
            errors['empty_first'] = "Please put in your first name."
        elif len(postData['registered_first_name']) < 2:
            errors['first_name_error'] = 'The first name has to be at least 2 characters.'

        if (len(postData['registered_last_name'])) == 0:
            errors['empty_last'] = "Please put in your last name."
        elif len(postData['registered_last_name']) < 2:
            errors['last_name_error'] = 'The last name has to be at least 2 characters.'

        if (len(postData['registered_email'])) == 0:
            errors['empty_email'] = "Please put in your email."
        elif not EMAIL_REGEX.match(postData['registered_email']):         
            errors['email'] = "Invalid email address!"

        if (len(postData['registered_password'])) == 0:
            errors['empty_pw'] = "Please put in your password."
        elif len(postData['registered_password']) < 8:
            errors['short_password'] = 'The password has to be at least 8 characters.'

        if postData['registered_password'] != postData['registered_confirm_pw']:
            errors['password_no_match'] = 'Your passwords do not match.'
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.TextField()
    password = models.CharField(max_length=64)
    objects = UserManager()

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
    img = models.ImageField(upload_to='')

class Review(models.Model):
    value = models.IntegerField()
    description = models.TextField()
    product = models.ForeignKey(
        Product,
        related_name="reviews",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name="reviews",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    quantity_in_cart = models.IntegerField()
    total_price = models.DecimalField(decimal_places=2, max_digits=5)

    product = models.ForeignKey(
        Product,
        related_name = "cart",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name="carts",
        on_delete=models.CASCADE
    )

class Order(models.Model):
    quantity_ordered = models.IntegerField()
    total_price = models.DecimalField(decimal_places=2, max_digits=5)

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
