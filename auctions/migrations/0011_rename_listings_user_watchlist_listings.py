# Generated by Django 4.0.2 on 2022-03-26 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_user_listings_delete_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='listings',
            new_name='watchlist_listings',
        ),
    ]
