# Generated by Django 4.2.11 on 2024-06-06 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0008_alter_post_thumbnail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="thumbnail",
            field=models.ImageField(
                blank=True, null=True, upload_to="", verbose_name="썸네일"
            ),
        ),
    ]
