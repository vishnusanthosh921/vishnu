# Generated by Django 4.2.7 on 2023-12-03 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productid', models.IntegerField()),
                ('usr', models.CharField(max_length=50)),
                ('quantity', models.IntegerField(default=1)),
            ],
        ),
    ]