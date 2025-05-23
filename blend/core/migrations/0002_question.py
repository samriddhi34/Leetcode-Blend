# Generated by Django 5.1.6 on 2025-03-15 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
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
                ("question_id", models.IntegerField(unique=True)),
                ("title", models.CharField(max_length=255)),
                ("acceptance_rate", models.IntegerField(default=0)),
                ("isPremium", models.BooleanField()),
                (
                    "difficulty",
                    models.CharField(
                        choices=[("E", "Easy"), ("M", "Medium"), ("H", "Hard")],
                        max_length=10,
                    ),
                ),
                ("urls", models.URLField()),
                ("solution_url", models.URLField(blank=True, null=True)),
                ("topics", models.JSONField(default=list)),
            ],
        ),
    ]
