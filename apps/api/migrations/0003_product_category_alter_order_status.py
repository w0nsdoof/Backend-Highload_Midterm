# Generated by Django 5.1.2 on 2024-10-20 11:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='api.category'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Created'), ('PAID', 'Paid'), ('SHIPPED', 'Shipped'), ('DELIVERED', 'Delivered'), ('FINISHED', 'Finished'), ('CANCELLED', 'Cancelled')], default='CREATED', max_length=100),
        ),
    ]
