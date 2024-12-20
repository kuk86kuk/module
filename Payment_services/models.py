from django.db import models

class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "В ожидании"),
        ("success", "Успешно"),
        ("failed", "Ошибка"),
    ]

    payment_id = models.CharField(max_length=64, unique=True, verbose_name="Идентификатор платежа")
    account_number = models.CharField(max_length=20, verbose_name="Номер счета")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма платежа")
    purpose = models.TextField(verbose_name="Назначение платежа")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending", verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Платеж {self.payment_id} на сумму {self.amount} руб."