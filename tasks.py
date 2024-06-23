import os
from pathlib import Path

from robocorp import log
from robocorp.tasks import task
from RPA.Robocorp.WorkItems import WorkItems

from src.application.exceptions.ItemError import ItemError
from src.application.utils.DateUtils import DateUtils
from src.domain.Item import Item
from src.application.automations.LATimesAutomation import LATimesAutomation

OUTPUT_DIR = Path(os.environ.get('ROBOT_ARTIFACTS'))

@task
def main():
    """
    Solve the RPA challenge
    
    Downloads the source data excel and uses Playwright to solve rpachallenge.com from challenge
    """
    
    log.info('Starting process')
    
    workitem = WorkItems()
    
    workitem.get_input_work_item()
    
    automation = LATimesAutomation()
    automation.open()
    
    for item in workitem.inputs:
        try:
            payload = item.payload
            payload_item = Item(search=payload['search'], topic=payload['topic'], months=int(payload['months']))
            
            automation.search(search_term=payload_item.search)
            automation.select_topic(topic=payload_item.topic)
            automation.sort_by(value='Newest')
            news = automation.get_data(date_until=DateUtils.define_month(months=payload_item.months))
            automation.to_excel(news, path=f'{OUTPUT_DIR}/output.xlsx')
            
        except ItemError as e:
            log.exception(f'Item error: {e}')
            item.fail(code="ITEM_INVALID", message=str(e))
            
        except Exception as e:
            log.exception(f'Error: {e}')
            item.fail(str(e))
            
    
    print('Done')