# Generated by Django 4.2.9 on 2024-02-09 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_buynow_payment_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='name',
            new_name='product_name',
        ),
    ]
