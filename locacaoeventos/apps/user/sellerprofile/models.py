from django.db import models

from django.contrib.auth.models import User

class SellerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation = models.DateTimeField(auto_now_add=True)
    name = models.CharField("Nome", max_length=64)
    email = models.CharField("E-mail", max_length=64)
    cellphone = models.CharField("Celular", max_length=64)

    cpf = models.CharField("CPF", max_length=32)
    cnpj = models.CharField("CNPJ", max_length=32)


    is_active = models.BooleanField(default=True)
    key = models.CharField("Secret Key", max_length=64, null=True, blank=True)
    accepts_newsletter = models.BooleanField()
    def __str__(self):
        return self.name