from robocorp import browser
from robocorp.tasks import task
from RPA.Excel.Files import Files as Excel

from pathlib import Path
import os
import requests
from RPA.Browser.Selenium import Selenium

from src.application.services.LATimes import LATimesAutomation

@task
def main():
    """
    Solve the RPA challenge
    
    Downloads the source data excel and uses Playwright to solve rpachallenge.com from challenge
    """
    
    automation = LATimesAutomation()
    automation.open()
    automation.search("Champions League2")
    
    print('Done')