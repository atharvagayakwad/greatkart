# Generated by Django 3.2.7 on 2022-01-20 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('store', '0003_productmodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductModel',
            new_name='Product',
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
    ]