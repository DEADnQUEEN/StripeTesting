from django.contrib import admin
from StripeApp import models, forms


class ItemInline(admin.StackedInline):
    model = models.OrderItem
    extra = 0
    autocomplete_fields = ['item']


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    form = forms.CurrencyAdminForm
    list_display = ['name', 'short_key']
    search_fields = ['name']
    ordering = ['id']


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_view', 'short_description', 'currency_name']
    list_filter = ['price', 'currency']
    search_fields = ['name']
    ordering = ['id']
    autocomplete_fields = ['currency']


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'item_name', 'quantity']
    ordering = ['id']
    search_fields = ['item_name']
    autocomplete_fields = ['item']


@admin.register(models.Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'percent']
    list_filter = ['percent']
    search_fields = ['name']
    ordering = ['id']


@admin.register(models.Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'percent']
    list_filter = ['percent']
    ordering = ['id']
    search_fields = ['name']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_discount', 'order_tax', 'price']
    autocomplete_fields = ['discount', 'tax']
    inlines = [ItemInline]
