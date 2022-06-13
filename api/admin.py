from django.contrib import admin
from .models import *

admin.site.register(Militant)
admin.site.register(Address)
admin.site.register(Core)
admin.site.register(DeclarationDate)
admin.site.register(PaymentDeclaration)
admin.site.register(PaymentDate)
admin.site.register(Payment)
admin.site.register(PaymentNorm)

