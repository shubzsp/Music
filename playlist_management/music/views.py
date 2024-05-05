from rest_framework.response import Response
from music.serializers import PlaylistSerializer, PlaylistListSerializer
from rest_framework import viewsets, status
from music.models import Playlist, MusicPlayList, Music


class PlaylistApiView(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistListSerializer

    def retrieve(self, request, *args, **kwargs):
        playlist = self.get_object()
        data = PlaylistSerializer(playlist).data
        return Response(data)

    def create(self, request, *args, **kwargs):
        data = request.data
        playlist_name = data.get('name')
        music_ids = data.get('music',[])
        if not playlist_name:
            return Response({"error":"Name can not be null"}, status=status.HTTP_400_BAD_REQUEST)
        playlist = Playlist.objects.create(name=playlist_name)
        added_songs = []
        order = 1
        for music_id in music_ids:
            if music_id in added_songs:
                continue
            MusicPlayList.objects.create(
                playlist=playlist,
                music_id=music_id,
                order=order
            )
            added_songs.append(music_id)
            order += 1
        data = PlaylistSerializer(playlist).data
        return Response(data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        playlist_name = data.get('name')
        music_ids = data.get('music')
        playlist = self.get_object()
        if playlist_name is not None:
            playlist.name = playlist_name
            playlist.save()
        if music_ids is not None:
            old_ids = MusicPlayList.objects.filter(playlist=playlist)
            music_to_remove = old_ids.exclude(music_id__in=music_ids)
            music_to_remove.delete()
            added_songs = []
            order = 1
            for music_id in music_ids:
                if music_id in added_songs:
                    continue
                if not Music.objects.filter(id=music_id).exists():
                    continue
                if not MusicPlayList.objects.filter(
                        playlist=playlist,
                        music_id=music_id,
                        order=order
                ).exists():
                    MusicPlayList.objects.filter(
                        playlist=playlist,
                        order=order
                    ).update(order=-order)
                    try:
                        music_playlist = MusicPlayList.objects.get(
                            playlist=playlist,
                            music_id=music_id,
                        )
                        music_playlist.order = order
                        music_playlist.save()
                    except MusicPlayList.DoesNotExist:
                        MusicPlayList.objects.create(
                            playlist=playlist,
                            music_id=music_id,
                            order=order
                        )
                added_songs.append(music_id)
                order += 1
        data = PlaylistSerializer(playlist).data
        return Response(data, status=status.HTTP_200_OK)
