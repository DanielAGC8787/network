# Generated by Django 4.0.4 on 2022-05-11 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_remove_post_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='timeStamp',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
    ]
