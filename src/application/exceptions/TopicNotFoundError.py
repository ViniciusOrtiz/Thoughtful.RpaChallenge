from src.application.exceptions.CustomError import CustomError

class TopicNotFoundError(CustomError):
    def __init__(self, message: str):
        super().__init__(message, 'TOPIC_NOT_FOUND')