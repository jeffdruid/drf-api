# Generated by Django 4.2.16 on 2024-10-25 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("moderation", "0003_alter_flaggedcontent_post_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="flaggedcontent",
            name="is_visible",
            field=models.BooleanField(default=False),
        ),
    ]