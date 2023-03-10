# Generated by Django 3.1.3 on 2022-03-20 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20220320_0126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('PENDING', 'P'), ('SHIPPED', 'S'), ('OUT FOR DELEVERY', 'O'), ('CANCELLED', 'C'), ('DELEVERED', 'D')], default='PENDING', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('P', 'PENDING'), ('S', 'SUCCES'), ('F', 'FAILED')], default='PENDING', max_length=20),
        ),
    ]
