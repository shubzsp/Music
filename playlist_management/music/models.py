from django.db import models


class Music(models.Model):
    name = models.CharField(max_length=200)


class Playlist(models.Model):
    name = models.CharField(max_length=200)
    music = models.ManyToManyField(Music, through='MusicPlayList')


class MusicPlayList(models.Model):
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        unique_together = [["playlist", "music"],["playlist", "order"]]
        ordering = ['order']

