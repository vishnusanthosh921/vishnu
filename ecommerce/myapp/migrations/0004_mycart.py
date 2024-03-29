# Generated by Django 4.2.7 on 2023-12-13 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='mycart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('delivered', models.BooleanField(default=False)),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.products')),
                ('usr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.usersignup')),
            ],
        ),
    ]
