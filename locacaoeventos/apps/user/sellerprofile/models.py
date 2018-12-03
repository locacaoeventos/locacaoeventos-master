from django.db import models

from django.contrib.auth.models import User

class SellerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation = models.DateTimeField(auto_now_add=True)
    name = models.CharField("Nome", max_length=30)
    email = models.CharField("E-mail", max_length=64)
    cellphone = models.CharField("Celular", max_length=64)

    cpf = models.CharField("CPF", max_length=32)
    cnpj = models.CharField("CNPJ", max_length=32)


    is_active = models.BooleanField(default=True)
    key = models.CharField("Secret Key", max_length=64, null=True, blank=True)
    accepts_newsletter = models.BooleanField()


    # Pagarme
    has_finished_payment = models.BooleanField(default=False)
    pagarme_id = models.CharField("ID Pagarme", max_length=64, null=True, blank=True, default="")
    bank_code = models.CharField("Código do Banco", max_length=3, null=True, blank=True, default="")
    agency = models.CharField("Agência", max_length=5, null=True, blank=True, default="")
    account = models.CharField("Conta Bancária", max_length=13, null=True, blank=True, default="")
    account_type = models.CharField("Tipo de Conta", max_length=32, null=True, blank=True, default="")
    def __str__(self):
        return self.name