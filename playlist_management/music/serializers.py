from rest_framework import serializers
from music.models import Playlist, Music, MusicPlayList

class PlaylistListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Playlist
        fields = ["id","name"]



class PlaylistSerializer(serializers.ModelSerializer):
    music = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ["id", "name", "music"]

    def get_music(self,obj):
        res = []
        music_playlist = MusicPlayList.objects.filter(
            playlist=obj
            )
        for music in music_playlist:
            res.append({"id":music.music.id, "name":music.music.name, "order":music.order})
        return res
