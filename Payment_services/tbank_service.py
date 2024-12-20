import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG)

class TBankService:
    BASE_URL = "https://business.tbank.ru/openapi/sandbox"
    SANDBOX_TOKEN = "TBankSandboxToken"

    @staticmethod
    def perform_payment(payment_data):
        """
        Выполнение платежа через API Т-Банка в песочнице.
        """
        url = f"{TBankService.BASE_URL}/secured/api/v1/payment/ruble-transfer/pay"
        headers = {
            "Authorization": f"Bearer {TBankService.SANDBOX_TOKEN}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payment_data))
            logging.debug(f"Отправленные данные: {payment_data}")
            logging.debug(f"Ответ от сервера: {response.status_code}, {response.text}")
            response.raise_for_status()  # Выбрасывает исключение, если статус ответа не 200-299

            # Проверка на пустое тело ответа
            if response.text:
                return response.json()
            else:
                return {"status": "success", "message": "Платеж успешно выполнен, но тело ответа пустое"}

        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при выполнении платежа: {e}")
            return None


    @staticmethod
    def get_statement(account_number, from_date, to_date=None):
        """
        Получение выписки по счету в песочнице.
        """
        url = f"{TBankService.BASE_URL}/api/v1/statement"
        headers = {
            "Authorization": f"Bearer {TBankService.SANDBOX_TOKEN}",
            "Content-Type": "application/json",
        }
        params = {
            "accountNumber": account_number,
            "from": from_date,
        }
        if to_date:
            params["to"] = to_date

        try:
            response = requests.get(url, headers=headers, params=params)
            logging.debug(f"Отправленные параметры: {params}")
            logging.debug(f"Ответ от сервера: {response.status_code}, {response.text}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при получении выписки: {e}")
            return None

# # Пример данных для платежа
# payment_data = {
#     "id": "unique_payment_id_123",
#     "from": {
#         "accountNumber": "12345678901234567890"
#     },
#     "to": {
#         "name": "ООО Получатель",
#         "inn": "7707083893",  # Исправленный ИНН
#         "kpp": "123456789",
#         "bik": "044525225",
#         "bankName": "Банк Получателя",
#         "corrAccountNumber": "30101810400000000225",
#         "accountNumber": "98765432109876543210"
#     },
#     "purpose": "Оплата заказа №123",
#     "amount": 1000.50,
#     "dueDate": "2024-12-25T12:00:00Z"
# }
# # Пример данных для получения выписки
# account_number = "12345678901234567890"
# from_date = "2023-01-01T00:00:00Z"
# to_date = "2023-12-31T23:59:59Z"

# # Выполнение платежа
# result = TBankService.perform_payment(payment_data)
# print(result)
# if result:
#     print("Платеж успешно выполнен:", result)
# else:
#     print("Ошибка при выполнении платежа")

