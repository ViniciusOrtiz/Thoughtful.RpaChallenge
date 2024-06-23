
from datetime import datetime
from dateutil.relativedelta import relativedelta

class DateUtils():
    
    @staticmethod
    def timestamp_to_datetime(timestamp: int) -> datetime:
        """
        Convert a timestamp to a datetime object

        Args:
            timestamp (int): Timestamp in seconds

        Returns:
            datetime: Date from timestamp
        """
        return datetime.fromtimestamp(timestamp)
    
    @staticmethod
    def define_month(months: int):
        """
        Subtracts a given number of months from the current date
        and returns the first day and hour of the resulting month. 

        Args:
            months (int): Number of months to subtract

        Returns:
            datetime: The first day of the resulting month
        """
        current_date = datetime.now()
        
        if(months < 2):
            return current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        new_date = current_date - relativedelta(months=months)
        first_day_of_month = new_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return first_day_of_month