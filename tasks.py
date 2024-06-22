from robocorp import browser
from robocorp.tasks import task
from RPA.Robocorp.WorkItems import WorkItems

from application.services.LATimesAutomation import LATimesAutomation

@task
def main():
    """
    Solve the RPA challenge
    
    Downloads the source data excel and uses Playwright to solve rpachallenge.com from challenge
    """
    workitem = WorkItems()
    
    workitem.get_input_work_item()
    
    automation = LATimesAutomation()
    automation.open()
    
    for item in workitem.work_items:
        automation.search("Champions League2")
    
    print('Done')