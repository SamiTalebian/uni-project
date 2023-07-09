from django.contrib import admin

from Auction.models import Contract, CustomUser, Transition

admin.site.register(Contract)
admin.site.register(CustomUser)
admin.site.register(Transition)
