import logging
import os
from pathlib import Path
import traceback

from robocorp import log
from robocorp.tasks import task
from robocorp import workitems

from src.application.automations.LATimesAutomation import LATimesAutomation
from src.application.exceptions.CustomError import CustomError
from src.domain.Item import Item
from src.application.utils.DateUtils import DateUtils

OUTPUT_DIR = Path(os.environ.get("ROBOT_ARTIFACTS"))
logging.basicConfig(level=logging.INFO)

@task
def main():
    """
    Solve the RPA challenge
    
    Downloads the source data excel and uses Playwright to solve rpachallenge.com from challenge
    """
    
    logging.info("Starting process")
    
    automation = LATimesAutomation()
    automation.open()
    
    for item in workitems.inputs:
        try:
            automation.navigate_home()
            payload = item.payload
            output_excel = payload['output.excel'] if 'output.excel' in payload else 'output.xlsx'
            
            logging.info(f"Processing payload: {payload}")
            
            payload_item = Item(
                search=payload["search"], topic=payload["topic"], 
                months=int(payload["months"]), file_name=output_excel)
            
            automation.search(search_term=payload_item.search)
            automation.select_topic(topic=payload_item.topic)
            automation.sort_by(value="Newest")
            news = automation.get_data(date_until=DateUtils.define_month(months=payload_item.months))
            automation.download_news_image(news=news, output_dir=OUTPUT_DIR)
            automation.to_excel(file=f"{OUTPUT_DIR}/{payload_item.file_name}", data=news, search=payload_item.search)
            
            logging.info(f"Process finished for search: {payload_item.search}")
            
        except CustomError as e:
            stacktrace = traceback.format_exc()
            logging.exception(f"Error: {str(stacktrace)}")
            item.fail(code=e.error_code, message=str(e), exception_type=str(type(e)))
            
        except Exception as e:
            stacktrace = traceback.format_exc()
            logging.exception(f"Error: {str(stacktrace)}")
            item.fail(code="UNEXPECTED_ERROR", message=str(e), exception_type=str(type(e)))
            
            #Restart the browser if an error occurs
            automation.close()
            automation.open()
            
    