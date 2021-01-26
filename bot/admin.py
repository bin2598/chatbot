from django.contrib import admin
from .models import register, chat

admin.site.register(register)
admin.site.register(chat)