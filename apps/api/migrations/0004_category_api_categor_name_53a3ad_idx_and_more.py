# Generated by Django 5.1.2 on 2024-10-20 12:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_product_category_alter_order_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name'], name='api_categor_name_53a3ad_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['customer'], name='api_order_custome_c4b878_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['status'], name='api_order_status_dee4b6_idx'),
        ),
        migrations.AddIndex(
            model_name='orderitem',
            index=models.Index(fields=['order', 'product'], name='api_orderit_order_i_faeaf1_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['category', 'name'], name='api_product_categor_3a8b28_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['price'], name='api_product_price_b6b1d7_idx'),
        ),
    ]
