from src.application.exceptions.ItemError import ItemError


class Item():
    def __init__(self, search: str, topic: str, months: int, file_name: str) -> None:
        """
        Domain class for an Item and validations

        Args:
            search (str): Search term
            topic (str): Topic to search
            months (int): Months to search

        Raises:
            ItemError: Some value is invalid
        """
        if(not isinstance(search, str)):
            raise ItemError('search must be a string')
        
        if(not isinstance(topic, str)):
            raise ItemError('topic must be a string')
        
        if(not isinstance(months, int)):
            raise ItemError('months must be an integer')
        
        if(not isinstance(file_name, str)):
            raise ItemError('file_name must be a string')
        
        if(not search):
            raise ItemError('search cannot be empty')
        
        if(not topic):
            raise ItemError('topic cannot be empty')
        
        if(months < 1):
            raise ItemError('months must be greater than 0')
        
        if(not file_name):
            raise ItemError('file_name cannot be empty')
        
        self.search = search
        self.topic = topic
        self.months = months
        self.file_name = file_name