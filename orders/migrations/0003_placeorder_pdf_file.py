# Generated by Django 4.2.6 on 2023-11-08 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_placeorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='placeorder',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='order_pdf'),
        ),
    ]