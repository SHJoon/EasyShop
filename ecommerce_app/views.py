from django.shortcuts import render, redirect
from django.contrib import messages

from .models import *
from .forms import ProductForm
import bcrypt

# Create your views here.
def login_index(request):

    return render(request, 'login.html')

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
    user_list = User.objects.filter(email=request.POST['login_email'])
    if len(user_list) == 0:
        messages.error(request, "Please check your email/password")
        return redirect("/login_index")

    if not bcrypt.checkpw(request.POST['login_password'].encode(), user_list[0].password.encode()):
        print("failed password")
        messages.error(request, "Please check your email/password")
        return redirect("/login_index")

    request.session['user_id'] = user_list[0].id
    return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/login_index")

# Function to display the main page
def homepage(request):
    context = {
        # "logged_in_user": User.objects.get(id=request.session['user_id']),
        "all_categories": Category.objects.all()
        
    }
    return render(request, "homepage.html", context)

# Function to display the shopping cart
def view_cart(request):
    context = {
        "logged_in_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, "cart.html", context)

def remove_from_cart(request, order_id):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    order_to_remove = Order.objects.get(id=order_id)

    logged_in_user.carts.remove(order_to_remove)

    return redirect("/cart")

def view_products(request, category_id):
    category = Category.objects.get(id=category_id)
    context = {
        "all_products": category.products.all()
    }

    return render(request, "", context)

def view_product_info(request, product_id):
    context={
        "this_product": Product.objects.get(id=product_id)
    }
    return render(request, "", context)

def post_review(request):
    logged_in_user: User.objects.get(id=request.session['user_id'])
    
    add_review = Review.objects.create(
        user = current_user,
        post=request.POST["post"]
    )
    return redirect("")













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


def process(request):

    product = Product.objects.get(id=int(request.POST["id"]))

    quantity_from_form = int(request.POST["quantity"])
    price_from_form = float(product.price)
    total_charge = quantity_from_form * price_from_form
    
    print("Charging credit card...")
    this_order = Order.objects.create(
        quantity_ordered = quantity_from_form,
        total_price = total_charge
        )
    
    request.session["order_id"] = this_order.id

    return redirect(f"checkout/{this_order.id}")


def order_comp(request, order_id):
    this_order = Order.objects.get(id=order_id)

    sum = 0
    count = 0

    all_orders = Order.objects.all()

    for curr_order in all_orders:
        sum += curr_order.total_price
        count += curr_order.quantity_ordered

    context ={
        "total_charge": this_order.total_price,
        "total_amadon_spent": sum,
        "total_quantity_bought": count 
    }

    return render(request, "order-complete.html", context)