# Generated by Django 3.2 on 2023-03-25 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank_accounts', '0004_bankaccount_nip_incorrect'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankaccount',
            name='withdraw',
        ),
    ]
