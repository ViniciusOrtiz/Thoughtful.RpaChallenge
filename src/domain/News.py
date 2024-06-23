from datetime import datetime
from pathlib import Path

class News():
    def __init__(self, title: str, description: str, date: datetime, image_url: Path) -> None:
        self.title = title
        self.description = description
        self.date = date
        self.image_url = image_url
        
    def to_json(self):
        return {
            'title': self.title,
            'description': self.description,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'image_url': self.image_url
        }