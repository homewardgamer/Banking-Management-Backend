# Generated by Django 4.0.4 on 2022-04-27 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_transaction_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]
