from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
from .tbank_service import TBankService

@csrf_exempt
def create_payment(request):
    """
    Представление для создания платежа.
    """
    if request.method == "POST":
        payment_data = {
            "id": request.POST.get("payment_id"),
            "from": {
                "accountNumber": request.POST.get("account_number"),
            },
            "to": {
                "accountNumber": request.POST.get("receiver_account_number"),
                "inn": request.POST.get("receiver_inn"),
                "kpp": request.POST.get("receiver_kpp"),
                "bankBic": request.POST.get("receiver_bank_bic"),
                "bankName": request.POST.get("receiver_bank_name"),
                "bankCorrAccount": request.POST.get("receiver_bank_corr_account"),
            },
            "purpose": request.POST.get("purpose"),
            "amount": float(request.POST.get("amount")),
            "dueDate": request.POST.get("due_date"),
        }

        # Выполнение платежа через API
        response = TBankService.perform_payment(payment_data)

        if response and response.get("status") == "success":
            # Сохранение платежа в базе данных
            Payment.objects.create(
                payment_id=payment_data["id"],
                account_number=payment_data["from"]["accountNumber"],
                amount=payment_data["amount"],
                purpose=payment_data["purpose"],
                status="success",
            )
            return JsonResponse({"message": "Платеж успешно создан"}, status=201)
        else:
            return JsonResponse({"error": "Ошибка при выполнении платежа"}, status=500)
    else:
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)


@csrf_exempt
def get_account_statement(request):
    """
    Представление для получения выписки по счету.
    """
    if request.method == "GET":
        account_number = request.GET.get("accountNumber")
        from_date = request.GET.get("from")
        to_date = request.GET.get("to")

        if not account_number or not from_date:
            return JsonResponse({"error": "Необходимы параметры accountNumber и from"}, status=400)

        response = TBankService.get_statement(account_number, from_date, to_date)

        if response:
            return JsonResponse(response, status=200)
        else:
            return JsonResponse({"error": "Ошибка получения выписки"}, status=500)
    else:
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)