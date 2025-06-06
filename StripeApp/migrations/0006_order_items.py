# Generated by Django 4.2.21 on 2025-06-02 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StripeApp', '0005_remove_order_items_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='order_items', through='StripeApp.OrderItem', to='StripeApp.item', verbose_name='Предметы в заказе'),
        ),
    ]
