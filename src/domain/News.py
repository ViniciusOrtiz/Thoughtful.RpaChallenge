from datetime import datetime

class News():
    def __init__(self, title: str, description: str, date: datetime) -> None:
        self.title = title
        self.description = description
        self.date = date
        
    def to_json(self):
        return {
            'title': self.title,
            'description': self.description,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S')
        }