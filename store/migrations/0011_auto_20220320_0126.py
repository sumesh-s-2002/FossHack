# Generated by Django 3.1.3 on 2022-03-20 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_order_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('P', 'PENDING'), ('S', 'SHIPPED'), ('O', 'OUT FOR DELEVERY'), ('C', 'CANCELLED'), ('D', 'DELEVERED')], default='PENDING', max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('P', 'PENDING'), ('S', 'SUCCES'), ('F', 'FAILED')], default='PENDING', max_length=1),
        ),
    ]
