# Generated by Django 4.1.4 on 2023-01-09 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_staff",
        ),
        migrations.AlterField(
            model_name="user",
            name="tag",
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(db_index=True, max_length=32),
        ),
    ]
