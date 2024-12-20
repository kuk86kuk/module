from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponse
from .entities.MoySkladApi import *

# Замените ваши логин и пароль на реальные, но только для тестирования!
# В продакшне используйте OAuth 2.0!
MOYSKLAD_LOGIN = "admin@egort123"
MOYSKLAD_PASSWORD = "egor86"
MOYSKLAD_BASE_URL =  "https://api.moysklad.ru/api/remap/1.2" # Замените на ваш базовый URL

def moysklad(request):
    return render(request, 'moysklad/moysklad.html')

def get_moysklad_client(entity_client_class):
    return entity_client_class(MOYSKLAD_LOGIN, MOYSKLAD_PASSWORD, MOYSKLAD_BASE_URL, verify_ssl=False)

def get_products_images(request, product_id=None, images_id=None):
    client = get_moysklad_client(ProductClient_IMAGES)
    if images_id!=None:
        return handle_api_request(request, client, 'GET', id=product_id, images_id=images_id)
    return handle_api_request(request, client, 'GET', id=product_id)

def images(request, product_id=None, images_id=None):
    client = get_moysklad_client(Images)
    response_data = client.get(images_id)
    return  HttpResponse(response_data, content_type="image/png")

# Products
def get_products(request, product_id=None):
    client = get_moysklad_client(ProductClient)
    if product_id!=None:
        return handle_api_request(request, client, 'GET', id=product_id)
    return handle_api_request(request, client, 'GET')

def create_product(request):
    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),
            "price": request.POST.get("price"),
            "description": request.POST.get("description"),
            "image_url": request.POST.get("image_url"),
            "stock": request.POST.get("stock"),
        }
        client = get_moysklad_client(ProductClient)
        return handle_api_request(request, client, 'POST', data=data)
    return HttpResponseBadRequest("Invalid request method")

def update_or_delete_product(request, product_id):
    client = get_moysklad_client(ProductClient)
    if request.method == "PUT":
        data = {
            "name": request.POST.get("name"),
            "price": request.POST.get("price"),
            "description": request.POST.get("description"),
            "image_url": request.POST.get("image_url"),
            "stock": request.POST.get("stock"),
        }
        return handle_api_request(request, client, 'PUT', id=product_id, data=data)
    elif request.method == "DELETE":
        return handle_api_request(request, client, 'DELETE', id=product_id)
    return HttpResponseBadRequest("Invalid request method")




def handle_api_request(request, client, method, id=None, data=None):
    try:
        if method == 'GET':
            response_data = client.get(id)
        elif method == 'POST':
            response_data = client.post(data)
        elif method == 'PUT':
            response_data = client.put(id, data)
        elif method == 'DELETE':
            client.delete(id)
            return JsonResponse({"success": True})
        else:
            return HttpResponseBadRequest("Invalid request method")
        return JsonResponse(response_data)
    except Exception as e:
        print(f"Error during API request: {e}")
        return HttpResponseServerError(f"API request failed: {e}")


# Customer Order Views

def get_customer_orders(request):
    client = get_moysklad_client(CustomerOrderClient)
    return handle_api_request(request, client, 'GET')

def create_customer_order(request):
    if request.method == "POST":
        try:
            data = {
                'organization': request.POST.get('organization'),
                'agent': request.POST.get('agent'),
                'positions': request.POST.get('positions') #Это нужно парсить в json, если positions - это JSON строка
            }
            client = get_moysklad_client(CustomerOrderClient)
            return handle_api_request(request, client, 'POST', data=data)
        except Exception as e:
            return HttpResponseBadRequest(f"Invalid request data: {e}")
    else:
        return HttpResponseBadRequest("Invalid request method")

def update_or_delete_customer_order(request, order_id):
    client = get_moysklad_client(CustomerOrderClient)
    if request.method == "PUT":
        try:
            data = {
                'organization': request.POST.get('organization'),
                'agent': request.POST.get('agent'),
                'positions': request.POST.get('positions') #Это нужно парсить в json, если positions - это JSON строка
            }
            return handle_api_request(request, client, 'PUT', id=order_id, data=data)
        except Exception as e:
            return HttpResponseBadRequest(f"Invalid request data: {e}")
    elif request.method == "DELETE":
        return handle_api_request(request, client, 'DELETE', id=order_id)
    else:
        return HttpResponseBadRequest("Invalid request method")


# Counterparty Views
def get_counterparties(request):
    client = get_moysklad_client(CounterpartyClient)
    return handle_api_request(request, client, 'GET')

def create_counterparty(request):
    if request.method == "POST":
        try:
            data = {
                "name": request.POST.get("name"),
                "phone": request.POST.get("phone"),
                "email": request.POST.get("email"),
            }
            client = get_moysklad_client(CounterpartyClient)
            return handle_api_request(request, client, 'POST', data=data)
        except Exception as e:
            return HttpResponseBadRequest(f"Invalid data: {e}")
    else:
        return HttpResponseBadRequest("Invalid request method")

def update_or_delete_counterparty(request, counterparty_id):
    client = get_moysklad_client(CounterpartyClient)
    if request.method == "PUT":
        try:
            data = {
                "name": request.POST.get("name"),
                "phone": request.POST.get("phone"),
                "email": request.POST.get("email"),
            }
            return handle_api_request(request, client, 'PUT', id=counterparty_id, data=data)
        except Exception as e:
            return HttpResponseBadRequest(f"Invalid data: {e}")
    elif request.method == "DELETE":
        return handle_api_request(request, client, 'DELETE', id=counterparty_id)
    else:
        return HttpResponseBadRequest("Invalid request method")


# Общая функция для создания клиента
def get_moysklad_client(entity_client_class):
    return entity_client_class(MOYSKLAD_LOGIN, MOYSKLAD_PASSWORD, MOYSKLAD_BASE_URL, verify_ssl=False)

def handle_api_request(request, client, method, id=None, data=None):
    try:
        if method == 'GET':
            response_data = client.get(id)
        elif method == 'POST':
            response_data = client.post(data)
        elif method == 'PUT':
            response_data = client.put(id, data)
        elif method == 'DELETE':
            client.delete(id)
            return JsonResponse({"success": True})
        else:
            return HttpResponseBadRequest("Invalid request method")
        return JsonResponse(response_data)
    except Exception as e:
        print(f"Error during API request: {e}")
        return HttpResponseServerError(f"API request failed: {e}")

# Customers
def get_customers(request):
    client = get_moysklad_client(CustomerClient)
    return handle_api_request(request, client, 'GET')

def create_customer(request):
    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),
            "phone": request.POST.get("phone"),
            "email": request.POST.get("email"),
            "addresses": request.POST.get("addresses"),  # JSON строка
        }
        client = get_moysklad_client(CustomerClient)
        return handle_api_request(request, client, 'POST', data=data)
    return HttpResponseBadRequest("Invalid request method")

def update_or_delete_customer(request, customer_id):
    client = get_moysklad_client(CustomerClient)
    if request.method == "PUT":
        data = {
            "name": request.POST.get("name"),
            "phone": request.POST.get("phone"),
            "email": request.POST.get("email"),
            "addresses": request.POST.get("addresses"),  # JSON строка
        }
        return handle_api_request(request, client, 'PUT', id=customer_id, data=data)
    elif request.method == "DELETE":
        return handle_api_request(request, client, 'DELETE', id=customer_id)
    return HttpResponseBadRequest("Invalid request method")



# Остальные сущности (аналогично)
# Product Categories
def get_product_categories(request):
    client = get_moysklad_client(ProductCategoryClient)
    return handle_api_request(request, client, 'GET')

def create_product_category(request):
    if request.method == "POST":
        data = {"name": request.POST.get("name")}
        client = get_moysklad_client(ProductCategoryClient)
        return handle_api_request(request, client, 'POST', data=data)
    return HttpResponseBadRequest("Invalid request method")

def update_or_delete_product_category(request, category_id):
    client = get_moysklad_client(ProductCategoryClient)
    if request.method == "PUT":
        data = {"name": request.POST.get("name")}
        return handle_api_request(request, client, 'PUT', id=category_id, data=data)
    elif request.method == "DELETE":
        return handle_api_request(request, client, 'DELETE', id=category_id)
    return HttpResponseBadRequest("Invalid request method")

# Orders
def get_orders(request):
    client = get_moysklad_client(OrderClient)
    return handle_api_request(request, client, 'GET')

def create_order(request):
    if request.method == "POST":
        data = {
            "customer": request.POST.get("customer"),  # ID клиента
            "items": request.POST.get("items"),  # JSON строка с товарами
            "status": request.POST.get("status"),
            "delivery_info": request.POST.get("delivery_info"),  # JSON строка с информацией о доставке
            "payment_info": request.POST.get("payment_info"),  # JSON строка с информацией о платеже
        }
        client = get_moysklad_client(OrderClient)
        return handle_api_request(request, client, 'POST', data=data)
    return HttpResponseBadRequest("Invalid request method")

def update_or_delete_order(request, order_id):
    client = get_moysklad_client(OrderClient)
    if request.method == "PUT":
        data = {
            "customer": request.POST.get("customer"),  # ID клиента
            "items": request.POST.get("items"),  # JSON строка с товарами
            "status": request.POST.get("status"),
            "delivery_info": request.POST.get("delivery_info"),  # JSON строка с информацией о доставке
            "payment_info": request.POST.get("payment_info"),  # JSON строка с информацией о платеже
        }
        return handle_api_request(request, client, 'PUT', id=order_id, data=data)
    elif request.method == "DELETE":
        return handle_api_request(request, client, 'DELETE', id=order_id)
    return HttpResponseBadRequest("Invalid request method")

# Payment Methods
def get_payment_methods(request):
    client = get_moysklad_client(PaymentMethodClient)
    return handle_api_request(request, client, 'GET')

def create_payment_method(request):
    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),  # Название способа оплаты
            "description": request.POST.get("description"),  # Описание
        }
        client = get_moysklad_client(PaymentMethodClient)
        return handle_api_request(request, client, 'POST', data=data)
    return HttpResponseBadRequest("Invalid request method")

def update_or_delete_payment_method(request, method_id):
    client = get_moysklad_client(PaymentMethodClient)
    if request.method == "PUT":
        data = {
            "name": request.POST.get("name"),  # Название способа оплаты
            "description": request.POST.get("description"),  # Описание
        }
        return handle_api_request(request, client, 'PUT', id=method_id, data=data)
    elif request.method == "DELETE":
        return handle_api_request(request, client, 'DELETE', id=method_id)
    return HttpResponseBadRequest("Invalid request method")

# Shipping Methods
def get_shipping_methods(request):
    client = get_moysklad_client(ShippingMethodClient)
    return handle_api_request(request, client, 'GET')

def create_shipping_method(request):
    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),  # Название способа доставки
            "description": request.POST.get("description"),  # Описание
            "cost": request.POST.get("cost"),  # Стоимость доставки
        }
        client = get_moysklad_client(ShippingMethodClient)
        return handle_api_request(request, client, 'POST', data=data)
    return HttpResponseBadRequest("Invalid request method")

def update_or_delete_shipping_method(request, method_id):
    client = get_moysklad_client(ShippingMethodClient)
    if request.method == "PUT":
        data = {
            "name": request.POST.get("name"),  # Название способа доставки
            "description": request.POST.get("description"),  # Описание
            "cost": request.POST.get("cost"),  # Стоимость доставки
        }
        return handle_api_request(request, client, 'PUT', id=method_id, data=data)
    elif request.method == "DELETE":
        return handle_api_request(request, client, 'DELETE', id=method_id)
    return HttpResponseBadRequest("Invalid request method")

# Reviews
def get_reviews(request):
    client = get_moysklad_client(ReviewClient)
    return handle_api_request(request, client, 'GET')

def create_review(request):
    if request.method == "POST":
        data = {
            "product": request.POST.get("product"),  # ID товара
            "customer": request.POST.get("customer"),  # ID клиента
            "rating": request.POST.get("rating"),  # Оценка (например, 1-5)
            "comment": request.POST.get("comment"),  # Текст отзыва
        }
        client = get_moysklad_client(ReviewClient)
        return handle_api_request(request, client, 'POST', data=data)
    return HttpResponseBadRequest("Invalid request method")

def update_or_delete_review(request, review_id):
    client = get_moysklad_client(ReviewClient)
    if request.method == "PUT":
        data = {
            "product": request.POST.get("product"),  # ID товара
            "customer": request.POST.get("customer"),  # ID клиента
            "rating": request.POST.get("rating"),  # Оценка
            "comment": request.POST.get("comment"),  # Текст отзыва
        }
        return handle_api_request(request, client, 'PUT', id=review_id, data=data)
    elif request.method == "DELETE":
        return handle_api_request(request, client, 'DELETE', id=review_id)
    return HttpResponseBadRequest("Invalid request method")

# Shipping Addresses
def get_shipping_addresses(request):
    client = get_moysklad_client(ShippingAddressClient)
    return handle_api_request(request, client, 'GET')

def create_shipping_address(request):
    if request.method == "POST":
        data = {
            "customer": request.POST.get("customer"),  # ID клиента
            "address": request.POST.get("address"),  # Адрес доставки
            "city": request.POST.get("city"),
            "postal_code": request.POST.get("postal_code"),
            "country": request.POST.get("country"),
        }
        client = get_moysklad_client(ShippingAddressClient)
        return handle_api_request(request, client, 'POST', data=data)
    return HttpResponseBadRequest("Invalid request method")

def update_or_delete_shipping_address(request, address_id):
    client = get_moysklad_client(ShippingAddressClient)
    if request.method == "PUT":
        data = {
            "customer": request.POST.get("customer"),  # ID клиента
            "address": request.POST.get("address"),  # Адрес доставки
            "city": request.POST.get("city"),
            "postal_code": request.POST.get("postal_code"),
            "country": request.POST.get("country"),
        }
        return handle_api_request(request, client, 'PUT', id=address_id, data=data)
    elif request.method == "DELETE":
        return handle_api_request(request, client, 'DELETE', id=address_id)
    return HttpResponseBadRequest("Invalid request method")