# Generated by Django 4.2.11 on 2024-03-24 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Student",
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
                ("name", models.CharField(default="", max_length=30)),
                ("age", models.IntegerField(default=0)),
                ("major", models.CharField(default="", max_length=50)),
                ("gitid", models.CharField(default="", max_length=50)),
            ],
        ),
    ]
