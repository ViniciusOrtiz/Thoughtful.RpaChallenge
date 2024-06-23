import datetime

from RPA.Browser.Selenium import Selenium, By
from robocorp import storage
from robocorp import log

from src.application.utils.ExcelUtils import ExcelUtils
from src.domain.News import News
from src.application.utils.DateUtils import DateUtils

class LATimesAutomation():
    def __init__(self) -> None:
        self._browser = Selenium()
        
    def open(self):
        """
        Opens the LA Times website
        """
        
        url = storage.get_text("LaTimesUrl")
        log.info(f"Opening LA Times website: {url}")
        self._browser.open_available_browser(url=url)
        
    def search(self, search_term: str):
        """
        Search for a term in the LA Times website

        Args:
            search_term (str): Term to be searched
        """
        
        log.info(f"Searching for: {search_term}")
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
        
        log.info(f"Selecting topic: {topic}")
        selector_topic_locator = f"//div/label[span[text()='{topic}']]/input"
        self._browser.wait_until_element_is_enabled(locator=selector_topic_locator, timeout=5)
        self._browser.set_focus_to_element(locator=selector_topic_locator)
        self._browser.click_element(locator=selector_topic_locator)
        self._try_wait_loading(timeout=2)
      
    def sort_by(self, value: str = 'Newest'):
        """
        Sorts the search results by newest
        """
        
        log.info(f"Sorting by newest")
        selector_sort_by = "//label[span[text()='Sort by']]/select"
        self._browser.wait_until_element_is_enabled(locator=selector_sort_by, timeout=5)
        self._browser.select_from_list_by_label(selector_sort_by, (value))
        self._try_wait_loading(timeout=2)
    
    def get_data(self, date_until: datetime) -> list[News]:
        selector_results = "//ul[contains(@class, 'search-results-module-results-menu')]/li"
        selector_result_title = "//h3[contains(@class, 'promo-title')]"
        selector_result_description = "//p[contains(@class, 'promo-description')]"
        selector_result_timestamp = "//p[contains(@class, 'promo-timestamp')]"
        
        log.info(f"Getting data until: {date_until}")
        
        has_news = True
        
        list_news: list[News] = []
        while has_news:
            
            self._browser.wait_until_element_is_visible(locator=selector_results)
            
            results = self._browser.find_elements(selector_results)
            
            for result in results:
                title = result.find_element(By.XPATH, selector_result_title).text
                description = result.find_element(By.XPATH, selector_result_description).text
                timestamp_miliseconds = result.find_element(By.XPATH, selector_result_timestamp).get_attribute('data-timestamp')
                timestamp_seconds = int(timestamp_miliseconds) / 1000
                
                date = DateUtils.timestamp_to_datetime(timestamp=timestamp_seconds)
                if date < date_until:
                    log.info(f"Date is before the limit, stopping search")
                    has_news = False
                    break
                
                list_news.append(News(title=title, description=description, date=date))
            
            if(has_news is False):
                break
            
            self._next_page()
        
        return list_news
        
    def to_excel(self, file: str, data: list[News]):
        """
        Writes the data to an excel file

        Args:
            file (str): File name
            data (list[News]): List of news
        """
        
        log.info(f"Writing data to excel file: {file}")
        
        payload = [news.to_json() for news in data]
        headers = ['Title', 'Description', 'Date']
        
        # ExcelUtils.dict_to_excel(data=payload, path=file, headers=headers)
        
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
            log.info(f'Waiting for loading icon')
            self._browser.wait_until_element_is_visible(locator=selector_loading_icon, error="Loading icon not visible", timeout=timeout)
            self._browser.wait_until_element_is_not_visible(locator=selector_loading_icon)
        except:
            log.info(f'Loading icon not found')
        