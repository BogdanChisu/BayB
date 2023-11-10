# Generated by Django 4.2.6 on 2023-10-26 15:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0011_product_image_1_product_image_2_product_image_3"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(null=True, upload_to="product_pics"),
        ),
        migrations.AlterField(
            model_name="product",
            name="image_1",
            field=models.ImageField(null=True, upload_to="product_pics"),
        ),
        migrations.AlterField(
            model_name="product",
            name="image_2",
            field=models.ImageField(null=True, upload_to="product_pics"),
        ),
        migrations.AlterField(
            model_name="product",
            name="image_3",
            field=models.ImageField(null=True, upload_to="product_pics"),
        ),
    ]