import os
from googleapiclient.discovery import build


class Video:
    API_KEY = os.getenv('API_KEY')

    def __init__(self, video_id):
        self.channel = self.get_channel().videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=video_id
        ).execute()
        self.video_id = video_id
        self.video_url = 'https://www.youtube.com/' + self.video_id
        self.video_title = self.channel['items'][0]['snippet']['title']
        self.video_likes_count = self.channel['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.video_title}'

    def get_channel(self):
        return build('youtube', 'v3', developerKey=self.API_KEY)


class PLVideo(Video):
    def __init__(self, video_id, video_playlist_id):
        super().__init__(video_id)
        self.video_playlist_id = self.get_channel().playlistItems().list(playlistId=video_playlist_id,
                                                                         part='contentDetails',
                                                                         maxResults=1,
                                                                         videoId=video_id
                                                                         ).execute()
