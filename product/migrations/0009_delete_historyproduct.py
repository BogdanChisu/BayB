# Generated by Django 4.2.6 on 2023-10-22 14:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0008_remove_historyproduct_product"),
    ]

    operations = [
        migrations.DeleteModel(
            name="HistoryProduct",
        ),
    ]
