from moysklad.api_client import MoySkladBaseClient

class CounterpartyClient(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "counterparty", verify_ssl)

class ProductClient(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "product", verify_ssl)

class ProductClient_IMAGES(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "product", verify_ssl)

    def get(self, id=None, images_id=None):
        url = f"{self.base_url}/entity/{self.entity_name}{f'/{id}' if id else ''}/images{f'/{images_id}' if images_id else ''}"
        response = self.session.get(url, headers=self._get_auth_header())
        self._handle_response(response)
        return response.json()

class Images(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "download", verify_ssl)

    def get(self, id=None):
        url = f"{self.base_url}/download/{f'{id}' if id else ''}?miniature=true"
        response = self.session.get(url, headers=self._get_auth_header())
        return response.content


class InvoiceClient(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "invoiceout", verify_ssl)

class PurchaseOrderClient(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "purchaseorder", verify_ssl)

class StoreClient(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "store", verify_ssl)

class OrganizationClient(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "organization", verify_ssl)

class CustomerOrderClient(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "customerorder", verify_ssl)

    def create_customer_order(self, organization, agent, positions):
        data = {
            "organization": {"meta": {"href": organization}},
            "agent": {"meta": {"href": agent}},
            "positions": positions
        }
        return super().post(data)

class CustomerClient(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "customer", verify_ssl)

class ProductCategoryClient(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "productcategory", verify_ssl)

class ShoppingCartClient(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "shoppingcart", verify_ssl)

class OrderClient(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "order", verify_ssl)

    def create_order(self, customer, status):
        data = {
            "customer": {"meta": {"href": customer}},
            "status": status
        }
        return super().post(data)

class PaymentMethodClient(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "paymentmethod", verify_ssl)

    def create_payment_method(self, name):
        data = {
            "name": name
        }
        return super().post(data)

class ShippingMethodClient(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "shippingmethod", verify_ssl)

    def create_shipping_method(self, name):
        data = {
            "name": name
        }
        return super().post(data)

class ReviewClient(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "review", verify_ssl)

    def create_review(self, product, text):
        data = {
            "product": {"meta": {"href": product}},
            "text": text
        }
        return super().post(data)

class ShippingAddressClient(MoySkladBaseClient):
    def __init__(self, login, password, base_url, verify_ssl=True):
        super().__init__(login, password, base_url, "shippingaddress", verify_ssl)

    def create_shipping_address(self, customer, address):
        data = {
            "customer": {"meta": {"href": customer}},
            "address": address
        }
        return super().post(data)