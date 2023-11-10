# Generated by Django 4.2.6 on 2023-10-16 17:04

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("userextend", "0002_delete_businessuser"),
    ]

    operations = [
        migrations.CreateModel(
            name="History",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
