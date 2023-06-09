from django.contrib import admin

from Auction.models import Contract, ContractUser, Trasaction

admin.site.register(Contract)
admin.site.register(ContractUser)
admin.site.register(Trasaction)
