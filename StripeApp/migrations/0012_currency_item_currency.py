# Generated by Django 4.2.21 on 2025-06-02 04:14

from django.db import migrations, models
import django.db.models.deletion

import StripeApp.constraints


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Currency = apps.get_model("StripeApp", "Currency")
    db_alias = schema_editor.connection.alias
    for name, api_key in StripeApp.constraints.CURRENCY_CODE_CHOICES.items():
        Currency.objects.using(db_alias).create(
            name=name,
            public_api_code=api_key
        )



class Migration(migrations.Migration):

    dependencies = [
        ('StripeApp', '0011_alter_order_discount_alter_order_tax'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='USD', max_length=3, verbose_name='Валюта')),
                ('public_api_code', models.CharField(choices=[('rk_test_51RUcJKQWV56vHYpOomPp7pWwuON34CY7Cw1Yd2Wjk4AMfMif6qlzppJmuj2zPSODr7iifDk0KTQ0BhsHprwElwpt00y92r2a7X', 'RUB'), ('rk_test_51RUcJKQWV56vHYpO0fXKG0xl6AyYS1EZezIw5JfHaN3CCDEuHXtfDPsWXZOHUDjTyCZuB1ChlxktU9b73OTZIrdA00WZgA1pdg', 'USD')], max_length=107, verbose_name='Ключ валюты')),
            ],
            options={
                'verbose_name': 'Валюта',
                'verbose_name_plural': 'Валюты',
                'db_table': 'Currency',
            },
        ),
        migrations.RunPython(forwards_func),
        migrations.AddField(
            model_name='item',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='StripeApp.currency'),
            preserve_default=False,
        ),
    ]
