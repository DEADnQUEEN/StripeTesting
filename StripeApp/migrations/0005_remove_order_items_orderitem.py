# Generated by Django 4.2.21 on 2025-06-02 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StripeApp', '0004_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StripeApp.item', verbose_name='Предмет')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StripeApp.order', verbose_name='Заказ')),
            ],
            options={
                'db_table': 'OrderItem',
            },
        ),
    ]
