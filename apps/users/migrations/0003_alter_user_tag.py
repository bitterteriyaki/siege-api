# Generated by Django 4.1.4 on 2023-01-09 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_remove_user_is_staff_alter_user_tag_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="tag",
            field=models.SmallIntegerField(),
        ),
    ]
