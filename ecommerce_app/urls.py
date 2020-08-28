from django.urls import path
from . import views

urlpatterns = [
    path('login_index', views.login_index),
    path('register', views.register_user),
    path('login', views.login_user),
    path('logout', views.logout),
    path('', views.homepage),
    path('products/<int:category_id>', views.view_products),
    path('products/<int:category_id>/<int:product_id>', views.view_product_info),
    path('products/<int:category_id>/<int:product_id>/add_to_cart', views.add_to_cart),
    path('products/<int:category_id>/<int:product_id>/review', views.post_review),
    path('products/<int:category_id>/<int:product_id>/review/<int:review_id>/delete', views.delete_review),
    path('cart', views.cart),
    path('cart/update/<int:cart_id>', views.update_cart),
    path('cart/remove/<int:cart_id>', views.delete_cart),
    # path('cart/checkout', views.checkout),
    path('cart/process', views.process),
    path('cart/success', views.success),

    # URLs for admin
    path('admin', views.admin),
    path('admin/new', views.new_product),
    path('admin/products', views.admin_products),
    path('admin/orders', views.admin_orders),
    path('admin/products/<int:product_id>/edit', views.admin_edit_product),
    path('admin/products/<int:product_id>/update', views.admin_update_product),
    path('admin/products/<int:product_id>/delete', views.admin_delete_product),
]