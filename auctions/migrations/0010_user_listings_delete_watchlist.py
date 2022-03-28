# Generated by Django 4.0.2 on 2022-03-26 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_comments_comment_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='listings',
            field=models.ManyToManyField(blank=True, related_name='listings', to='auctions.AuctionListings'),
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
