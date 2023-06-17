from datetime import timedelta

import isodate

from src.video import Video


class PlayList(Video):
    def __init__(self, video_play_list_id):
        playlists = super().get_channel().playlists().list(id=video_play_list_id,
                                                           part='id,snippet',
                                                           ).execute()
        self.video_pla_list_id = video_play_list_id
        self.title = playlists['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={playlists['items'][0]['id']}"
        playlist_videos = super().get_channel().playlistItems().list(playlistId=video_play_list_id,
                                                                     part='contentDetails',
                                                                     maxResults=50,
                                                                     ).execute()
        playlist_videos_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        self.video_response = super().get_channel().videos().list(part='contentDetails,statistics',
                                                                  id=','.join(playlist_videos_ids)
                                                                  ).execute()

    @property
    def total_duration(self):
        duration = 0
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration).seconds
        return timedelta(seconds=duration)

    def show_best_video(self):
        max_liked = 0
        most_liked_video = 0
        for response in self.video_response['items']:
            if int(response['statistics']['likeCount']) > max_liked:
                most_liked_video = response['id']
                max_liked = int(response['statistics']['likeCount'])

        return f'https://youtu.be/{most_liked_video}'

