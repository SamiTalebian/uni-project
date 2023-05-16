from django.db import models

class ContractUser(models.Model):
    name = models.CharField()
    address = models.CharField()
    email = models.EmailField()
    contracts = models.ForeignKey('Contract',on_delete=models.SET_NULL,related_name='contract_users')
    
class Contract(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField()
    cost = models.FloatField()
    creator_address = models.CharField()

class Trasaction(models.Model):
    contract = models.OneToOneField(Contract,on_delete=models.SET_NULL)
    contract_user = models.OneToOneField(ContractUser,on_delete=models.SET_NULL)
    trasaction_date = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField()
    contract = models.OneToOneField(Contract, on_delete=models.SET_NULL)

