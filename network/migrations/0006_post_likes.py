# Generated by Django 4.0.4 on 2022-05-11 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_delete_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]