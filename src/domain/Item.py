from src.application.exceptions.ItemError import ItemError


class Item():
    def __init__(self, search: str, topic: str, months: int) -> None:
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
            raise ItemError('Search must be a string')
        
        if(not isinstance(topic, str)):
            raise ItemError('Topic must be a string')
        
        if(not isinstance(months, int)):
            raise ItemError('Months must be an integer')
        
        if(not search):
            raise ItemError('Search cannot be empty')
        
        if(not topic):
            raise ItemError('Topic cannot be empty')
        
        if(months < 1):
            raise ItemError('Months must be greater than 0')
        
        self.search = search
        self.topic = topic
        self.months = months