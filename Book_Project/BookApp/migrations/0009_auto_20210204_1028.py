# Generated by Django 3.1.5 on 2021-02-04 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookApp', '0008_auto_20210204_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(upload_to='images/placeholder.webp'),
        ),
    ]