import datetime
import logging
import os
from pathlib import Path
import urllib.parse
import requests

from RPA.Browser.Selenium import Selenium, By
from robocorp import storage
from robocorp import log

from src.application.utils.ExcelUtils import ExcelUtils
from src.application.utils.StringUtils import StringUtils
from src.domain.News import News
from src.application.utils.DateUtils import DateUtils

REGEX_MONEY_PATTERN = r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+ (?:dollars|USD)'

class LATimesAutomation():
    def __init__(self) -> None:
        self._browser = Selenium()
        self._base_url = storage.get_text("LaTimesUrl")
        
    def open(self):
        """
        Opens the LA Times website
        """
        
        logging.info(f"Opening LA Times website: {self._base_url}")
        self._browser.open_available_browser(url=self._base_url, headless=False)
        
    def navigate_home(self):
        """
        Navigates to the home page
        """
        
        logging.info(f"Navigating to home page")
        self._browser.go_to(url=self._base_url)
        
    def search(self, search_term: str):
        """
        Search for a term in the LA Times website

        Args:
            search_term (str): Term to be searched
        """
        
        logging.info(f"Searching for: {search_term}")
        selector_search_input = "//input[@placeholder='Please enter search term']"
        selector_search_button = "//div[contains(@class, 'search-results-module-query')]/button[span[text()='Search']]"
        
        self._browser.wait_until_element_is_visible(locator=selector_search_input)
        self._browser.input_text(locator=selector_search_input, text=search_term)
        self._browser.click_element(locator=selector_search_button)
        self._try_wait_loading(timeout=2)
        
    def select_topic(self, topic: str):
        """
        Selects a topic in the LA Times website

        Args:
            topic (str): Topic to be selected
        """
        
        logging.info(f"Selecting topic: {topic}")
        selector_topic_locator = f"//div/label[span[text()='{topic}']]/input"
        self._browser.wait_until_element_is_enabled(locator=selector_topic_locator, timeout=5)
        self._browser.set_focus_to_element(locator=selector_topic_locator)
        self._browser.click_element(locator=selector_topic_locator)
        self._try_wait_loading(timeout=2)
      
    def sort_by(self, value: str = 'Newest'):
        """
        Sorts the search results by newest
        """
        
        logging.info(f"Sorting by newest")
        selector_sort_by = "//label[span[text()='Sort by']]/select"
        self._browser.wait_until_element_is_enabled(locator=selector_sort_by, timeout=5)
        self._browser.select_from_list_by_label(selector_sort_by, (value))
        self._try_wait_loading(timeout=2)
    
    def get_data(self, date_until: datetime) -> list[News]:
        """
        Get news data from the search results until a certain date

        Args:
            date_until (datetime): Date until the data should be retrieved

        Returns:
            list[News]: List of news
        """
        selector_results = "//ul[contains(@class, 'search-results-module-results-menu')]/li"
        selector_result_title = ".//h3[contains(@class, 'promo-title')]"
        selector_result_description = ".//p[contains(@class, 'promo-description')]"
        selector_result_timestamp = ".//p[contains(@class, 'promo-timestamp')]"
        selector_image = ".//img[@class='image']"
        
        logging.info(f"Getting data until: {date_until}")
        
        has_news = True
        
        list_news: list[News] = []
        while has_news:
            
            self._browser.wait_until_element_is_visible(locator=selector_results)
            
            results = self._browser.find_elements(selector_results)
            
            for result in results:
                title = result.find_element(By.XPATH, selector_result_title)
                description = result.find_element(By.XPATH, selector_result_description)
                timestamp = result.find_element(By.XPATH, selector_result_timestamp)
                image = result.find_element(By.XPATH, selector_image)
                
                title_text = title.text if title is not None else ''
                description_text = description.text if description is not None else ''
                timestamp_time = timestamp.get_attribute('data-timestamp')
                image_url = urllib.parse.unquote(image.get_attribute('src'))
                
                timestamp_seconds = int(timestamp_time) / 1000
                
                date = DateUtils.timestamp_to_datetime(timestamp=timestamp_seconds)
                if date < date_until:
                    logging.info(f"Date is before the limit, stopping search")
                    has_news = False
                    break
                
                list_news.append(News(title=title_text, description=description_text, date=date, image_url=image_url))
            
            if(has_news is False):
                break
            
            self._next_page()
        
        return list_news
        
    def download_news_image(self, news: list[News], output_dir: str):
        """
        Download news images from 'image_url' and save them to output folder

        Args:
            news (list[News]): List of news
        """
        
        os.makedirs(output_dir, exist_ok=True)
        [os.remove(f'{output_dir}\{f}') for f in os.listdir(output_dir)]
        
        for n in news:
            image_url = n.image_url
            logging.info(f"Downloading image: {image_url}")
            
            response = requests.get(image_url)
            response.raise_for_status()
            
            file_name = os.path.basename(image_url)
            
            local_file = Path(output_dir, file_name)
            with open(local_file, 'wb') as f:
                f.write(response.content)
                
            logging.info(f"Image downloaded to: {local_file}")
        
    def to_excel(self, file: str, data: list[News], search: str):
        """
        Writes the data to an excel file

        Args:
            file (str): File name
            data (list[News]): List of news
        """
        
        logging.info(f"Writing data to excel file: {file}")
        
        file_dir = os.path.dirname(file)
        os.makedirs(file_dir, exist_ok=True)
        os.remove(file) if os.path.exists(file) else None
        
        news_dto = []
        
        for news in data:
            title_has_money = StringUtils.regex_match(regex=REGEX_MONEY_PATTERN, text=news.title)
            description_has_money = StringUtils.regex_match(regex=REGEX_MONEY_PATTERN, text=news.description)
            
            title_count = StringUtils.count_text(word=news.title, text=search)
            description_count = StringUtils.count_text(word=news.description, text=search)
            
            news_dto.append({
                'Title': news.title,
                'Date': news.date,
                'Description': news.description,
                'Image Filename': os.path.basename(news.image_url),
                'Count': title_count + description_count,
                'Has Money': True if title_has_money or description_has_money else False
            })
        
        ExcelUtils.dict_to_excel(data=news_dto, path=file)
        
    def _next_page(self):
        selector_next_page = "//a[span[text()='Next']]"
        url = self._browser.get_element_attribute(selector_next_page, 'href')
        self._browser.go_to(url)
        
    def _try_wait_loading(self, timeout: int = 5):
        """
        Try to wait for the loading icon to disappear.
        Because of website cache, the loading icon might not appear

        Args:
            timeout (int, optional): Timeout to wait loading. Defaults to 5.
        """
        selector_loading_icon = "//div[contains(@class, 'loading-icon')]"
        
        try:
            logging.info(f'Waiting for loading icon')
            self._browser.wait_until_element_is_visible(locator=selector_loading_icon, error="Loading icon not visible", timeout=timeout)
            self._browser.wait_until_element_is_not_visible(locator=selector_loading_icon)
        except:
            logging.info(f'Loading icon not found')
        