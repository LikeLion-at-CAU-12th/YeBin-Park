# Generated by Django 4.2.11 on 2024-06-05 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0006_alter_post_writer"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="thumbnail",
            field=models.ImageField(
                blank=True, null=True, upload_to="", verbose_name="썸네일"
            ),
        ),
    ]
