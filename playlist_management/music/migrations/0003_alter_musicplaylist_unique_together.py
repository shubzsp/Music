# Generated by Django 5.0.4 on 2024-05-04 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_rename_play_list_musicplaylist_playlist'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='musicplaylist',
            unique_together={('music', 'playlist'), ('playlist', 'order')},
        ),
    ]
