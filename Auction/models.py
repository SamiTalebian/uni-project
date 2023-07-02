from django.db import models

# class ContractUser(models.Model):
#     name = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255)
#     contracts = models.ForeignKey('Contract',on_delete=models.CASCADE,related_name='contract_users')

# class Contract(models.Model):
#     created_time = models.DateTimeField(auto_now_add=True)
#     finish_time = models.DateTimeField()
#     cost = models.FloatField()
#     creator_address = models.CharField(max_length=255)

# class Trasaction(models.Model):
#     contract = models.OneToOneField(Contract,on_delete=models.CASCADE)
#     contract_user = models.OneToOneField(ContractUser,on_delete=models.CASCADE)
#     trasaction_date = models.DateTimeField(auto_now_add=True)

# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     contract = models.OneToOneField(Contract, on_delete=models.CASCADE)


class Contract(models.Model):
    contract_address = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    min_bid = models.IntegerField()
    bidders = models.JSONField(default=list, null=True, blank=True)
    members = models.JSONField(default=list, null=True, blank=True)
    public_auction = models.BooleanField(default=False)

    def __str__(self):
        return self.contract_address
