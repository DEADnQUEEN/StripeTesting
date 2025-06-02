from django.db import models
from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator
from StripeApp import constraints


class Currency(models.Model):
    name = models.CharField(
        max_length=constraints.CURRENCY_CODE_CHARS,
        verbose_name="Валюта",
        default=constraints.DEFAULT_CURRENCY
    )
    public_api_code = models.CharField(
        choices=(
            (key, currency)
            for currency, key in constraints.CURRENCY_CODE_CHOICES.items()
        ),
        verbose_name='Ключ валюты',
        max_length=constraints.API_KEY_LENGTH
    )

    @property
    @admin.display(empty_value='Ключа нет', description="Ключ API")
    def short_key(self):
        return constraints.cut_text(self.public_api_code)

    class Meta:
        db_table = 'Currency'
        verbose_name = 'Валюта'
        verbose_name_plural = "Валюты"

    def __str__(self):
        return f"Валюта: {self.name}"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.public_api_code = constraints.CURRENCY_CODE_CHOICES[self.name]
        super(Currency, self).save(force_insert, force_update, using, update_fields)


class Item(models.Model):
    name = models.CharField(
        verbose_name='Название предмета',
        max_length=constraints.MAX_NAME_LENGTH,
    )
    price = models.IntegerField(
        verbose_name='Цена'
    )
    description = models.CharField(
        verbose_name='Описание предмета',
        max_length=constraints.MAX_DESCRIPTION_LENGTH,
        blank=True
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
    )

    @property
    @admin.display(description='Валюта')
    def currency_name(self):
        return self.currency.name

    @property
    @admin.display(description='Описание', empty_value='Нет описания')
    def short_description(self):
        return constraints.cut_text(self.description)

    @property
    @admin.display(description="Цена", empty_value='Нет цены')
    def price_view(self):
        return f"{constraints.setup_dots(self.price)} {self.currency.name}"

    class Meta:
        db_table = 'Item'
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return f'Предмет "{self.name}", цена: {self.price}'


class Discount(models.Model):
    name = models.CharField(
        max_length=constraints.MAX_NAME_LENGTH,
        verbose_name="Название скидки"
    )
    percent = models.DecimalField(
        validators=[
            MaxValueValidator(constraints.MAX_DISCOUNT),
            MinValueValidator(constraints.MIN_DISCOUNT)
        ],
        max_digits=5,
        decimal_places=2,
        verbose_name='Процент'
    )

    class Meta:
        db_table = 'Discount'
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Tax(models.Model):
    name = models.CharField(
        max_length=constraints.MAX_NAME_LENGTH,
        verbose_name="Название налога"
    )
    percent = models.DecimalField(
        validators=[
            MaxValueValidator(constraints.MAX_DISCOUNT),
            MinValueValidator(constraints.MIN_DISCOUNT)
        ],
        max_digits=5,
        decimal_places=2,
        verbose_name='Процент'
    )

    class Meta:
        db_table = 'Tax'
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'


class Order(models.Model):
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_discount',
        blank=True
    )
    tax = models.ForeignKey(
        Tax,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_tax',
        blank=True
    )

    @property
    @admin.display(empty_value='Нет скидки', description='Скидка')
    def order_discount(self):
        return self.discount.percent if self.discount else None

    @property
    @admin.display(empty_value='Нет налогов', description='Налоги')
    def order_tax(self):
        return self.tax.percent if self.tax else None

    @property
    @admin.display(empty_value='Нет товаров', description='Стоимость товаров')
    def price(self):
        if not self.rel_order.count():
            return None

        cash = 0
        for order_item in self.rel_order.all():
            cash += order_item.price

        if self.discount:
            cash = round(
                cash * (constraints.PERCENTS - self.discount.percent) / constraints.PERCENTS,
                constraints.NUMBERS_AFTER_DOT
            )

        if self.tax:
            cash = round(
                cash * (constraints.PERCENTS + self.tax.percent) / constraints.PERCENTS,
                constraints.NUMBERS_AFTER_DOT
            )

        return cash

    def __str__(self):
        return f'Заказ №{self.id}'

    class Meta:
        db_table = 'Order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        on_delete=models.CASCADE,
        related_name='rel_order'
    )
    item = models.ForeignKey(
        Item,
        verbose_name='Предмет',
        on_delete=models.CASCADE,
        related_name='order_item'
    )
    quantity = models.IntegerField(
        default=1,
        verbose_name='Количество'
    )

    class Meta:
        db_table = 'OrderItem'
        verbose_name = 'Вещь в заказе'
        verbose_name_plural = 'Вещи в заказе'

    def __str__(self):
        return f'{str(self.item)}, Количество: {self.quantity}'

    @property
    @admin.display(description="Предмет")
    def item_name(self):
        return self.item.name

    @property
    def price(self):
        return self.item.price * self.quantity

    @property
    @admin.display(description='Номер заказа')
    def order_number(self):
        return self.order.id
