# Generated by Django 4.0.4 on 2022-06-22 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_post_liked_alter_post_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
