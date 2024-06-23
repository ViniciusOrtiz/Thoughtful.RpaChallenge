from src.application.exceptions.CustomError import CustomError

class ItemError(CustomError):
    def __init__(self, message: str):
        super().__init__(message, 'ITEM_ERROR')