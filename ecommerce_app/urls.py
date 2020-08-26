from django.urls import path
from . import views

urlpatterns = [
    path('login_index', views.login_index),
    path('register', views.register_user),
    path('login', views.login_user),
    path('logout', views.logout),
    path('', views.homepage),

    # URLs for admin
    path('admin', views.admin),
    path('admin/new', views.new_product),
    path('admin/products', views.admin_products),
    path('admin/orders', views.admin_orders),
    path('admin/products/<int:product_id>/edit', views.admin_edit_product),
    path('admin/products/<int:product_id>/update', views.admin_update_product),
    path('admin/products/<int:product_id>/delete', views.admin_delete_product),
]