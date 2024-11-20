# Generated by Django 4.2.16 on 2024-11-03 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("moderation", "0004_flaggedcontent_is_visible"),
    ]

    operations = [
        migrations.CreateModel(
            name="TriggerWord",
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
                ("word", models.CharField(max_length=100, unique=True)),
                ("category", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]