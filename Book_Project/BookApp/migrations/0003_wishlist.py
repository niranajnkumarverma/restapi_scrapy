# Generated by Django 3.0.5 on 2021-01-27 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BookApp', '0002_auto_20210125_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BookApp.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BookApp.User')),
            ],
        ),
    ]