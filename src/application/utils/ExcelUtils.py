import pandas as pd

class ExcelUtils():
    
    @staticmethod
    def dict_to_excel(data: list[dict], path: str, headers: list[str] = None):
        """
        Writes a list of dictionaries to an excel file
        
        Args:
            data (list[dict]): List of dictionaries
            path (str): File path
            headers (list[str]): Headers for the excel file
        """
        
        df = pd.DataFrame(data)
        
        if(headers is not None):
            df.columns = headers
            
        df.to_excel(path, index=False)