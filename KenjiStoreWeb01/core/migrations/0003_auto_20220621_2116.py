# Generated by Django 3.2.13 on 2022-06-22 01:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_boletaitem_cantidad'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boleta',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='boletaitem',
            old_name='boleta_id',
            new_name='boleta',
        ),
        migrations.RenameField(
            model_name='boletaitem',
            old_name='item_id',
            new_name='item',
        ),
    ]
