# Generated by Django 3.2.7 on 2022-02-07 19:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0005_variationmodel'),
        ('orders', '0002_auto_20220127_0133'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderPlacedModel',
            new_name='OrderProductModel',
        ),
        migrations.AlterModelOptions(
            name='orderproductmodel',
            options={'verbose_name': 'Order Product', 'verbose_name_plural': 'Order Product'},
        ),
    ]
