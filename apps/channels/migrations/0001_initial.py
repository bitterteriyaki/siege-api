# Generated by Django 4.1.4 on 2023-02-01 21:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("guilds", "0004_alter_guild_members_delete_guildmember"),
    ]

    operations = [
        migrations.CreateModel(
            name="Channel",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=128)),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "guild",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="channels",
                        to="guilds.guild",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
                "abstract": False,
            },
        ),
    ]
