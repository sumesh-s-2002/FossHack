# Generated by Django 3.1.3 on 2022-03-20 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20220319_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, to='store.customer'),
            preserve_default=False,
        ),
    ]
