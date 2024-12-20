from django.urls import path
from .views import *

urlpatterns = [
    path('', moysklad, name='moysklad'),

    path('products/', get_products, name='get_products'),
    path('products/create/', create_product, name='create_product'),
    path('products/<str:product_id>/', get_products, name='get_products'),
    path('products/<str:product_id>/images', get_products_images, name='get_products_images'),
    path('products/<str:product_id>/images/<str:images_id>', images, name='images'),
    # Customer Orders
    path('customer-orders/', get_customer_orders, name='get_customer_orders'),
    path('customer-orders/create/', create_customer_order, name='create_customer_order'),
    path('customer-orders/<int:order_id>/', update_or_delete_customer_order, name='update_or_delete_customer_order'),

    # Counterparties
    path('counterparties/', get_counterparties, name='get_counterparties'),
    path('counterparties/create/', create_counterparty, name='create_counterparty'),
    path('counterparties/<int:counterparty_id>/', update_or_delete_counterparty, name='update_or_delete_counterparty'),

    # New entities
    path('customers/', get_customers, name='get_customers'),
    path('customers/create/', create_customer, name='create_customer'),
    path('customers/<int:customer_id>/', update_or_delete_customer, name='update_or_delete_customer'),

    path('products/', get_products, name='get_products'),
    path('products/create/', create_product, name='create_product'),
    path('products/<int:product_id>/', update_or_delete_product, name='update_or_delete_product'),

    path('product-categories/', get_product_categories, name='get_product_categories'),
    path('product-categories/create/', create_product_category, name='create_product_category'),
    path('product-categories/<int:category_id>/', update_or_delete_product_category, name='update_or_delete_product_category'),

    path('orders/', get_orders, name='get_orders'),
    path('orders/create/', create_order, name='create_order'),
    path('orders/<int:order_id>/', update_or_delete_order, name='update_or_delete_order'),

    path('payment-methods/', get_payment_methods, name='get_payment_methods'),
    path('payment-methods/create/', create_payment_method, name='create_payment_method'),
    path('payment-methods/<int:method_id>/', update_or_delete_payment_method, name='update_or_delete_payment_method'),

    path('shipping-methods/', get_shipping_methods, name='get_shipping_methods'),
    path('shipping-methods/create/', create_shipping_method, name='create_shipping_method'),
    path('shipping-methods/<int:method_id>/', update_or_delete_shipping_method, name='update_or_delete_shipping_method'),

    path('reviews/', get_reviews, name='get_reviews'),
    path('reviews/create/', create_review, name='create_review'),
    path('reviews/<int:review_id>/', update_or_delete_review, name='update_or_delete_review'),

    path('shipping-addresses/', get_shipping_addresses, name='get_shipping_addresses'),
    path('shipping-addresses/create/', create_shipping_address, name='create_shipping_address'),
    path('shipping-addresses/<int:address_id>/', update_or_delete_shipping_address, name='update_or_delete_shipping_address'),
]