from django.contrib import admin
from .models import Pessoa, Token, Balance, History


admin.site.register(Pessoa)
admin.site.register(Token)
admin.site.register(Balance)
admin.site.register(History)
