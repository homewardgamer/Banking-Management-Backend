# Generated by Django 4.0.4 on 2022-04-26 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_rename_branch_id_user_branch'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Transactions',
            new_name='Transaction',
        ),
    ]
