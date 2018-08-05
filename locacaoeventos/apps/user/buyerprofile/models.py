from django.db import models

from django.contrib.auth.models import User

class BuyerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Usuário Comprador+")
    name = models.CharField("Nome", max_length=64)
    birthday = models.DateField()

    cellphone = models.CharField("Celular", max_length=64)
    gender = models.CharField("Sexo", max_length=64)
    civil_status = models.CharField("Status Civil", max_length=64)

    creation = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    key = models.CharField("Secret Key", max_length=64, null=True, blank=True)
    email = models.CharField("E-mail", max_length=64)
    photo = models.FileField('Foto', upload_to='buyerprofile/photo', null=True, blank=True)

    creation = models.DateTimeField(auto_now_add=True)
    accepts_newsletter = models.BooleanField()

    def __str__(self):
        return self.name

class FamilyMember(models.Model):
    gender = models.CharField("Sexo", max_length=64)
    name = models.CharField("Nome", max_length=64)

    birthday = models.DateField()

    related_to = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, related_name="Parentesco com+")
