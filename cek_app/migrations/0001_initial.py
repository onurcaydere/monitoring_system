# Generated by Django 4.1.1 on 2022-09-12 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Car",
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
                ("cmd_input", models.TextField()),
                ("cmd_output", models.TextField()),
            ],
        ),
    ]
