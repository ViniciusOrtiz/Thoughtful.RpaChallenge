import os
from pathlib import Path

from robocorp import log
from robocorp.tasks import task
from robocorp import workitems

from src.application.automations.LATimesAutomation import LATimesAutomation
from src.application.exceptions.CustomError import CustomError
from src.application.exceptions.TopicNotFoundError import TopicNotFoundError
from src.domain.Item import Item
from src.application.utils.DateUtils import DateUtils
from src.application.exceptions.ItemError import ItemError

OUTPUT_DIR = Path(os.environ.get('ROBOT_ARTIFACTS'))
OUTPUT_FILE_XLSX = f'{OUTPUT_DIR}/output.xlsx'
OUTPUT_IMAGE_DIR = f'{OUTPUT_DIR}/images'

@task
def main():
    """
    Solve the RPA challenge
    
    Downloads the source data excel and uses Playwright to solve rpachallenge.com from challenge
    """
    
    log.info('Starting process')
   
    automation = LATimesAutomation()
    automation.open()
    
    for item in workitems.inputs:
        try:
            automation.navigate_home()
            payload = item.payload
            payload_item = Item(search=payload['search'], topic=payload['topic'], months=int(payload['months']))
            
            automation.search(search_term=payload_item.search)
            automation.select_topic(topic=payload_item.topic)
            automation.sort_by(value='Newest')
            news = automation.get_data(date_until=DateUtils.define_month(months=payload_item.months))
            automation.download_news_image(news=news, output_dir=payload['output_images'])
            automation.to_excel(file=payload['output_excel'], data=news, search=payload_item.search)
            
            log.info(f'Process finished for search: {payload_item.search}')
            
        except CustomError as e:
            log.exception(f'Error: {str(e)}')
            item.fail(code=e.error_code, message=str(e))
            
        except Exception as e:
            log.exception(f'Error: {str(e)}')
            item.fail(code="UNEXPECTED_ERROR", message=str(e))
            
    