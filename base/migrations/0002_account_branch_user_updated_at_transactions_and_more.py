# Generated by Django 4.0.4 on 2022-04-26 05:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('account_type', models.CharField(default='savings', max_length=300, verbose_name='account_type')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='balance')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('branch_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('branch_name', models.CharField(max_length=300)),
                ('branch_address', models.CharField(max_length=500)),
                ('branch_code', models.IntegerField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('transaction_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=300)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('r_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='r_transactions', to='base.account')),
                ('s_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='s_transactions', to='base.account')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='account_holder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='branch_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.branch'),
        ),
    ]
