# Generated by Django 4.2.6 on 2023-11-17 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_item', models.BooleanField(default=False)),
                ('wishlist_item', models.BooleanField(default=False)),
                ('quantity', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlaceOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_list', models.JSONField(null=True)),
                ('order_number', models.CharField(max_length=50)),
                ('delivery_address', models.TextField(max_length=100)),
                ('invoice_address', models.TextField(max_length=100)),
                ('price', models.CharField(max_length=100)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='order_pdf')),
                ('created_at', models.DateTimeField()),
            ],
        ),
    ]
