from django.contrib import admin
from .models import CardModel, OrderHistoryModel

admin.site.register(CardModel)
admin.site.register(OrderHistoryModel)
