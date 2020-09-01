from django.shortcuts import render, redirect
from django.contrib import messages

from .models import *
from .forms import ProductForm
import bcrypt

admin_id = [1,4,5]
# Create your views here.
def login_index(request):

    return render(request, 'register.html')

# Function to handle registration
def register_user(request):
    all_errors = User.objects.validator(request.POST)

    if len(all_errors) > 0:
        for _, val in all_errors.items():
            messages.error(request, val)
        return redirect('/login_index')

    password = request.POST['registered_password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    try:
        created_user = User.objects.create(
            first_name = request.POST['registered_first_name'],
            last_name = request.POST['registered_last_name'],
            email = request.POST['registered_email'],
            password = pw_hash
        )
    except:
        messages.error(request, "You can't use that email address.")
        return redirect("/login_index")
        
    request.session['user_id'] = created_user.id

    return redirect('/')

# Functions for handling login
def login_user(request):
    user_list = User.objects.filter(email=request.POST['email'])
    if len(user_list) == 0:
        messages.error(request, "Please check your email/password")
        return redirect("/login_index")

    if not bcrypt.checkpw(request.POST['password'].encode(), user_list[0].password.encode()):
        print("failed password")
        messages.error(request, "Please check your email/password")
        return redirect("/login_index")

    request.session['user_id'] = user_list[0].id
    return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

# Function to display the main page
def homepage(request):
    try:
        User.objects.get(id=request.session['user_id'])
        is_logged_in = True
    except:
        is_logged_in = False
    is_admin = False
    if is_logged_in:
        if request.session["user_id"] in admin_id:
            is_admin=True

    context = {
        "all_categories": Category.objects.all(),
        "is_logged_in": is_logged_in,
        "is_admin": is_admin,
    }
    return render(request, "homepage.html", context)

def view_products(request, category_id):
    try:
        User.objects.get(id=request.session['user_id'])
        is_logged_in = True
    except:
        is_logged_in = False

    category = Category.objects.get(id=category_id)
    context = {
        "is_logged_in": is_logged_in,
        "category": category
    }

    return render(request, "products.html", context)

def view_product_info(request, category_id, product_id):
    this_product = Product.objects.get(id=product_id)
    try:
        User.objects.get(id=request.session['user_id'])
        is_logged_in = True
    except:
        is_logged_in = False
    
    sum = 0
    if len(this_product.reviews.all()) != 0:
        for review in this_product.reviews.all():
            sum += review.value
        avg_review = round((sum) / len(this_product.reviews.all()))
    else:
        avg_review = 0

    context={
        "this_product": this_product,
        "avg_review": avg_review,
        "is_logged_in": is_logged_in,
        "category_id": category_id,
    }
    return render(request, "product-info.html", context)

def post_review(request, category_id, product_id):    
    Review.objects.create(
        value = request.POST['review_val'],
        description = request.POST['review'],
        product = Product.objects.get(id=product_id),
        user = User.objects.get(id=request.session['user_id'])
    )
    return redirect(f"/products/{category_id}/{product_id}")

def delete_review(request, category_id, product_id, review_id):
    Review.objects.get(id=review_id).delete()

    return redirect(f"/products/{category_id}/{product_id}")

def add_to_cart(request, category_id, product_id):
    product = Product.objects.get(id=product_id)
    total_price = float(request.POST['quantity']) * float(product.price)
    Cart.objects.create(
        quantity_in_cart = request.POST['quantity'],
        total_price = total_price,
        product = product,
        user = User.objects.get(id=request.session['user_id']),
    )
    return redirect(f"/cart")

def cart(request):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view that page.")
        return redirect("/login_index")

    logged_user = User.objects.get(id=request.session['user_id'])
    all_carts = Cart.objects.filter(user = logged_user)
    total_sum = 0
    for item in all_carts:
        total_sum += item.total_price
    context = {
        "total_sum": total_sum,
        "all_carts": all_carts,
        "logged_user": logged_user,
    }

    return render(request, "check-out.html", context)

def update_cart(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.quantity_in_cart = request.POST["quantity"]
    cart.total_price = float(cart.quantity_in_cart) * float(cart.product.price)

    cart.save()

    return redirect("/cart")

def delete_cart(request, cart_id):
    Cart.objects.get(id=cart_id).delete()

    return redirect("/cart")


# def checkout(request):
#     if "user_id" not in request.session:
#         messages.error(request, "You must be logged in to view that page.")
#         return redirect("/")

#     all_carts = Cart.objects.all()
#     total_sum = 0
#     for item in all_carts:
#         total_sum += item.total_price
#     context = {
#         "total_sum": total_sum
#     }

#     return render(request, "check-out.html", context)

def process(request):
    logged_user = User.objects.get(id=request.session['user_id'])
    cart = Cart.objects.filter(user = logged_user)
    count = 0
    for item in cart:
        count += item.quantity_in_cart
        Order.objects.create(
            quantity_ordered = item.quantity_in_cart,
            total_price = item.total_price,
            purchased_user = logged_user,
            purchased_product = item.product
        )
        item.delete()
    request.session['count'] = count
    return redirect(f"/cart/success")

def success(request):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view that page.")
        return redirect("/")

    context={
        'num_items': request.session['count']
    }
    return render(request, "checkout-success.html", context)


# Functions relating to admins
def admin(request):
    context={
        'all_categories': Category.objects.all(),
        'all_products': Product.objects.all(),
        'all_orders': Order.objects.all(),
        'all_carts': Cart.objects.all(),
        'all_reviews': Review.objects.all(),
    }
    return render(request, "admin/admin.html", context)

def new_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        print(request.POST.getlist('category'))
        if form.is_valid():
            new_prod = form.save()
            for cat_id in request.POST.getlist('category'):
                new_prod.categories.add(Category.objects.get(id=cat_id))
            if request.POST['other_cat'] != "":
                other_cat = Category.objects.create(category=request.POST['other_cat'])
                new_prod.categories.add(other_cat)
            return redirect("/admin")
    
    else:
        form = ProductForm()

    context = {
        "form": form,
        "all_categories": Category.objects.all()
    }
    return render(request, "admin/new_product.html", context)

def admin_products(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "admin/all_products.html", context)

def admin_orders(request):
    context = {
        "all_orders": Order.objects.all()
    }
    return render(request, "admin/all_orders.html", context)

def admin_edit_product(request, product_id):
    context = {
        "product": Product.objects.get(id=product_id)
    }
    return render(request, "admin/edit_product.html", context)

def admin_update_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.name = request.POST['name']
    product.price = request.POST['price']
    product.description = request.POST['description']

    all_cats = request.POST.getlist('category')
    for cat in product.categories.all():
        product.categories.remove(cat)
    for cat_id in all_cats:
        product.categories.add(Category.objects.get(id=cat_id))
        
    product.save()

    return redirect('/admin/products')

def admin_delete_product(request, product_id):
    Product.objects.get(id=product_id).delete()

    return redirect("/admin/products")
