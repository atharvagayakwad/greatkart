# Generated by Django 3.2.7 on 2022-01-19 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customermodel',
            name='user',
        ),
        migrations.RemoveField(
            model_name='orderplacedmodel',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='orderplacedmodel',
            name='product',
        ),
        migrations.RemoveField(
            model_name='orderplacedmodel',
            name='user',
        ),
        migrations.DeleteModel(
            name='CartModel',
        ),
        migrations.DeleteModel(
            name='CustomerModel',
        ),
        migrations.DeleteModel(
            name='OrderPlacedModel',
        ),
        migrations.DeleteModel(
            name='ProductModel',
        ),
    ]