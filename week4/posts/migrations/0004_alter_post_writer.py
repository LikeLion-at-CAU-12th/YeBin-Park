# Generated by Django 4.2.11 on 2024-05-09 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0003_alter_comment_created_at_alter_comment_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="writer",
            field=models.CharField(max_length=20, verbose_name="사용자명"),
        ),
    ]
