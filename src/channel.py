import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.url = self.channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.subscribers = self.channel['items'][0]['statistics']['subscriberCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']
        self.description = self.channel['items'][0]['snippet']['description']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other_channel):
        return int(self.subscribers) + int(other_channel.subscribers)

    def __sub__(self, other_channel):
        return int(self.subscribers) - int(other_channel.subscribers)

    def __gt__(self, other_channel):
        return int(self.subscribers) > int(other_channel.subscribers)

    def __lt__(self, other_channel):
        return int(self.subscribers) < int(other_channel.subscribers)

    def __ge__(self, other_channel):
        return int(self.subscribers) >= int(other_channel.subscribers)

    def __le__(self, other_channel):
        return int(self.subscribers) <= int(other_channel.subscribers)

    def __eq__(self, other_channel):
        return int(self.subscribers) == int(other_channel.subscribers)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            data = {
                'channel_id': self.channel_id,
                'title': self.title,
                'url': self.url,
                'video_count': self.video_count,
                'subscribers': self.subscribers,
                'view_count': self.view_count,
                'description': self.description
            }
            json.dump(data, f)
