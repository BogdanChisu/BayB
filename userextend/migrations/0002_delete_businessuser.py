# Generated by Django 4.2.6 on 2023-10-12 16:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("userextend", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="BusinessUser",
        ),
    ]