# Generated by Django 3.1.3 on 2022-03-18 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(default='download.jpg', upload_to=''),
        ),
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(default='download.jpg', upload_to=''),
        ),
    ]