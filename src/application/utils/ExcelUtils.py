# import pandas as pd

class ExcelUtils():
    
    @staticmethod
    def dict_to_excel(data: dict, path: str, headers: list[str] = None):
        """
        Save a model to an Excel file

        Args:
            model (pandas.DataFrame): Model to save
            path (str): Path to save the model
        """
        
        # if not isinstance(data, dict):
        #     raise TypeError("Parameter 'data' must be a dictionary.")
        
        # df = pd.DataFrame(data)
        
        # if(headers is not None):
        #     df.columns = headers
            
        # df.to_excel(path, index=False)