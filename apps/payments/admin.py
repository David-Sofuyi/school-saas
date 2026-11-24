from django.contrib import admin
from .models import SchoolBankAccount, PaymentEvidence, Payment, Receipt

admin.site.register(SchoolBankAccount)
admin.site.register(PaymentEvidence)
admin.site.register(Payment)
admin.site.register(Receipt)
